# Tradeshift Engine

Tradeshift Engine is a replay trading simulator built to help learners and retailers understand trading mechanics and experiment with trading strategies in a controlled, replayable environment. It recreates historical market data as a simulated real-time feed so users can backtest strategies, visualize performance, and compare different approaches as if trading in live markets.

Repository: https://github.com/Ritsham/tradeshift-engine

## Features

- Replay historical market data as a simulated real-time feed
- Run and compare multiple trading strategies
- Track portfolio and per-trade statistics
- Configurable replay speed and initial portfolio parameters
- Docker-friendly for easy deployments
- Extensible architecture to add new data feeds and strategies

## Tech stack

- Language: Python
- Container: Docker (Dockerfile included)

## Quick links

- Repository: [Ritsham/tradeshift-engine](https://github.com/Ritsham/tradeshift-engine)
- Default branch: `main`

---

## Getting started

These instructions will get a local copy of the project up and running for development and testing.

### Prerequisites

- Python 3.8+ (3.10 recommended)
- pip
- git
- (Optional) Docker & Docker Compose for containerized runs

### Recommended workflow (local)

1. Clone the repo
   ```
   git clone https://github.com/Ritsham/tradeshift-engine.git
   cd tradeshift-engine
   ```

2. Create and activate a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
   If a `requirements.txt` is not present yet, add the project dependencies (e.g., pandas, numpy, matplotlib, pytest).

4. Run the simulator (replace the command below with your actual entrypoint if different)
   ```
   python -m tradeshift_engine        # example module entrypoint
   # or
   python main.py                     # example script entrypoint
   ```

Notes:
- If you have a specific CLI or script (e.g., `run.py`, `simulate.py`), replace the example command above with the actual filename/module.

### Docker

To build and run using the included Dockerfile:

1. Build the image
   ```
   docker build -t tradeshift-engine .
   ```

2. Run a container (example, adjust environment variables and mounts as needed)
   ```
   docker run --rm -it \
     -v "$(pwd)/data:/app/data" \
     -e CONFIG_FILE=/app/config/config.yaml \
     tradeshift-engine
   ```

This will start the simulator inside the container. Adjust volumes and env vars per your configuration.

---




## Contributing

Contributions are welcome! A suggested CONTRIBUTING.md should include:

- How to set up a dev environment
- Branching and commit message guidelines
- How to run tests and linters
- How to submit pull requests

Basic steps:
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit changes and push: `git push origin feat/your-feature`
4. Open a Pull Request describing your changes

---

## Issues & support

Use the GitHub Issues for bug reports and feature requests:
https://github.com/Ritsham/tradeshift-engine/issues

If you want direct support or have questions, open an issue and tag `help wanted` or `question`.

---

## License

This repository currently does not specify a license. To make the project's license explicit, add a `LICENSE` file (for example, MIT, Apache-2.0, or another license). If you want, I can add a suggested license file.

---

## Acknowledgements

- Inspired by replay/backtesting platforms and tutorial projects for learning trading systems.
- Thanks to contributors and users who file issues and PRs.

---

If you want, I can:
- update the README with exact CLI commands and environment variables if you provide the main entrypoint filename and config names,
- add a sample `config.example.yaml`,
- produce a CONTRIBUTING.md or a CI workflow (GitHub Actions) to run tests automatically.

