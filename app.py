from server import run

if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=2000,
    )
    run(**config)
