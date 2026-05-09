import sys

from app import create_app


def main():
    app = create_app()
    sys.exit(app.run())


if __name__ == "__main__":
    main()