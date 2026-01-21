# client/client.py
from cli import parse_args
from uploader import upload_files


def main():
    args = parse_args(__import__("sys").argv)
    upload_files(args.host, args.port, args.files)


if __name__ == "__main__":
    main()
