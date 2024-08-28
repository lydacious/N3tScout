# N3tScout

**Note**: This project is currently under development.

N3tScout is a Python-based tool for running network reconnaissance and vulnerability scans. The tool provides a GUI for configuring and executing various scanning tools, such as `subfinder`, `httpx`, `subzy` and `dirsearch`.

## Features

- **Subfinder**: Discover subdomains for a given target.
- **HTTPX**: Check active subdomains and perform other HTTP-related scans.
- **Subzy**: Subdomain takeover tool which works based on matching response fingerprints from can-i-take-over-xyz.
- **Dirsearch**: Perform directory and file enumeration on active subdomains.

## Prerequisites

- **Python 3.6+**: Make sure you have Python 3.6 or higher installed.
- **Scanning Tools**: Ensure `subfinder`, `httpx`, `subzy` and `dirsearch` are installed and available in your system's PATH.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/lydacious/n3tscout.git
    cd n3tscout
    ```

2. **Install Dependencies**

    While this project does not have external Python dependencies currently, ensure that required scanning tools are installed:

    - Install `subfinder`, `httpx`, `subzy` and `dirsearch` as per their respective documentation.

3. **Running the Application**

    Run the application using the provided `startN3tScout.sh` script:

    ```bash
    ./startN3tScout.sh
    ```

    This script will set necessary permissions and start the N3tScout application.

## Usage

1. **Launch the Application**

    Execute the `startN3tScout.sh` script to start the GUI application.

2. **Configure and Run Scans**

    - Enter target domains or IPs in the input field.
    - Adjust the settings for `subfinder`, `httpx`, `subzy` and `dirsearch` as needed.
    - Click "Run" to start the scanning process.
    - Click "Stop" to terminate the ongoing scans.

3. **View Logs**

    The application provides a log section to view real-time output from the scans.

## Contributing

If you'd like to contribute to the project:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


**Note**: Ensure that you have the necessary permissions and licenses for any third-party tools or libraries you use.
