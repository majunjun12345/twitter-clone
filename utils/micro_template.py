"""
语法：

    1.支持通过点语法获取 dict 的键值，同时支持过滤器

        {{ var.modifer.modifier|filter|filter }}

    2. 循环

        {% for item in list %}...{% endfor %}

    3. if 语句

        {% if var(a bool type) %}...{% endif %}

    4. 注释

        {# This will be ignored #}


标准使用流程：

    1. 以原始文本为参数，创建实例

        template = Template('''
            <h1>Hello {{name|upper}}!</h1>
            {% for topic in topics %}
                <p>You are interested in {{topic}}.</p>
            {% endif %}
            ''',
            dict(
            upper=str.upper,
            <过滤器>=<过滤器函数对应的函数>
            ),
        )

    2. 调用 render(context) 方法，返回渲染过的文本。其中 context 是 dict 类型

        text = template.render(dict(
            name='Ned',
            topics=['Python', 'Geometry', 'Juggling'],
        ))
"""
import re


class TemplateSyntaxError(ValueError):
    """
    触发语法错误
    """
    pass


class CodeBuilder(object):
    """
    代码构建器，将模板编译为 Python 代码时所用工具的集合
    """
    
    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent
    
    def __str__(self):
        """
        返回所有代码
        """
        return "".join(str(c) for c in self.code)
    
    def add_line(self, line):
        """
        增加一行代码
        其中的 self.indent_level 自动生成

        一行代码的组成：
        <若干等级的缩进><代码正文><换行符 \n>
        """
        self.code.extend([" " * self.indent_level, line, "\n"])
    
    def add_placeholder(self):
        """
        add_placeholder 用于放置一个空的占位符，改占位符用于后来添加变量定义语句
        """
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section
    
    # 默认缩进 4 个空格
    INDENT_STEP = 4
    
    def indent(self):
        """
        增加缩进
        """
        self.indent_level += self.INDENT_STEP
    
    def dedent(self):
        """
        减少缩进
        """
        self.indent_level -= self.INDENT_STEP
    
    def get_globals(self):
        """
        运行代码，并返回 namespace dict
        """
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace


class MicroTemplate(object):
    """
    Template 类中的代码分为编译和渲染两个阶段
    """
    
    def __init__(self, text, *contexts):
        """
        text 是输入的模板
        context 是输入的数据于过滤器函数，可以输入多个 context
        """
        self.context = {}
        for context in contexts:
            self.context.update(context)
        
        self.all_variables = set()
        self.loop_variables = set()
        
        code = CodeBuilder()
        
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        # variables_code 用于占位
        variables_code = code.add_placeholder()
        code.add_line("result = []")
        
        buffered = []
        
        def flush_output():
            """
            分析模板时，分析的结果会暂存在一段缓冲区中，
            每分析完一段就会通过 flush_output 根据缓存的内容往 code 中添加新代码。
            """
            print('buffered in flush_output() '
                  'before code.add_line \n<{}>'.format(buffered))
            
            code.add_line("result.extend([{}])".format(", ".join(buffered)))
            
            print('code in flush_output() '
                  'after code.add_line \n<{}>'.format(code))
            del buffered[:]
        
        # ops_stack 检查代码嵌套是否正确
        ops_stack = []
        
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        
        for token in tokens:
            if token.startswith('{#'):
                # 注释；不作处理
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                buffered.append("str({})".format(expr))
            elif token.startswith('{%'):
                # 刷新缓存
                flush_output()
                words = token[2:-2].strip().split()
                if words[0] == 'if':
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", token)
                    ops_stack.append('if')
                    code.add_line("if {}:".format(self._expr_code(words[1])))
                    code.indent()
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    ops_stack.append('for')
                    self._variable(words[1], self.loop_variables)
                    code.add_line(
                        "for c_{} in {}:".format(
                            words[1],
                            self._expr_code(words[3])
                        )
                    )
                    code.indent()
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if len(ops_stack) == 0:
                        self._syntax_error("Too many ends", token)
                    
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error("Mismatched end tag", end_what)
                    code.dedent()
                else:
                    self._syntax_error("Don't understand tag", words[0])
            else:
                if len(token) != 0:
                    buffered.append(repr(token))
        
        # 检查栈 ops_stack 是否为空
        if ops_stack:
            self._syntax_error("Unmatched action tag", ops_stack[-1])
        
        # 将缓存刷新到结果之中
        flush_output()
        
        for var_name in self.all_variables - self.loop_variables:
            variables_code.add_line("c_{} = context[{!r}]".format(var_name, var_name))
        
        code.add_line("return ''.join(result)")
        code.dedent()
        self._render_function = code.get_globals()['render_function']
    
    def _expr_code(self, expression):
        """
        根据 expr 将模板内的表达式转换为 Python 表达式
        """
        if "|" in expression:
            pipes = expression.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_variables)
                code = "c_{}({})".format(func, code)
        elif "." in expression:
            dots = expression.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])
            code = "do_dots({}, {})".format(code, args)
        else:
            self._variable(expression, self.all_variables)
            code = "c_{}".format(expression)
        return code
    
    def _syntax_error(self, message, thing):
        """
        触发语法错误
        """
        raise TemplateSyntaxError("{}: {!r}".format(message, thing))
    
    def _variable(self, name, variables_set):
        """
        用于将变量存入指定的变量集中，
        同时可验证变量名的有效性，
        变量必须以 '_'或者大小写英文字母开头，只包含 '_' 大小写字母以及数字
        若变量名无效，触发语法错误
        """
        if re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            variables_set.add(name)
        else:
            self._syntax_error("Not a valid name", name)
    
    @staticmethod
    def _do_dots(value, *dots):
        """
        在编译阶段，一个模板表达式 "x.y.z" 会被编译成 do_dots(x, 'y', 'z')，

        html里面的点操作在 Python 中可能会有三种可能实现
        1: value = x['y']
        2: value = getattr(obj, "attribute")
            <=> value = obj.attribute
        3: value = value()
            用 callable 来测试 value 是否是能够调用的函数
        """
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value
    
    def render(self, **kwargs):
        """
        通过 context dict渲染模板
        context 是一个将值用于渲染的 dict
        """
        context = kwargs
        render_context = dict(self.context)
        if context is not None:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)
