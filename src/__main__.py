from main import app, disable_custom_redirect


def main() -> None:
    disable_custom_redirect()
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context="adhoc")


if __name__ == "__main__":
    main()
