# Contributions Guidelines

Thank you for your interest in contributing to our ETL tool! This project generates Python code using Jinja2, with FastAPI serving as the backend (and delivering JavaScript to the frontend). We welcome your input in code, documentation, issue reporting, and more.

---

## 1. Code of Conduct

All contributors are expected to adhere to our [Code of Conduct](/CODE_OF_CONDUCT.md). We strive to create a welcoming and respectful environment. Please ensure that your interactions and contributions are professional and constructive. Harassment, discrimination, or any unprofessional behavior will not be tolerated.

### Code of Conduct Details
- **Be respectful:** Treat all community members with courtesy and respect.
- **Be inclusive:** Encourage an environment where everyone feels welcome regardless of background or experience.
- **Be constructive:** Offer helpful, constructive feedback when reviewing contributions.
- **Report issues:** If you experience or witness any unacceptable behavior, please reach out to the project maintainers.

---

## 2. How to Contribute

There are many ways to contribute to the project:

- **Feature Development:** Submit new features or improvements.
- **Bug Fixes:** Identify and resolve bugs.
- **Documentation:** Improve our GitHub Wiki and inline documentation.
- **Issue Reporting:** Use the GitHub issue tracker to report bugs or propose enhancements.

Before starting, please search existing issues and the public wiki to see if your contribution is already being discussed or planned.

---

## 3. Reporting Issues

- **Use GitHub Issues:** When reporting a bug or suggesting an enhancement, please use the GitHub issue section.
- **Include Details:** Provide clear, reproducible steps, screenshots (if applicable), and any error messages. The more detail, the easier it will be for us to help resolve the issue.

---

## 4. Development Workflow & Branch Naming

Our project uses GitHub for version control. Please follow these guidelines for a smooth contribution process:

### Branch Naming Conventions

- **Feature Branches:** `feature/short-description`  
  (e.g., `feature/add-login-support`)
- **Bugfix Branches:** `bugfix/short-description`  
  (e.g., `bugfix/fix-date-parsing`)
- **Chore/Maintenance Branches:** `chore/short-description`  
  (e.g., `chore/update-dependencies`)

### Workflow Steps

1. **Fork & Clone:** Fork the repository on GitHub and clone it locally.
2. **Create a Branch:** Create a new branch following the naming conventions.
3. **Develop:** Make your changes, ensuring you follow our style guidelines (see below) and include tests where applicable.
4. **Commit:** Write clear, concise commit messages describing your changes.
5. **Pull Request (PR):** Submit your PR against the **staging** branch.

---

## 5. Pull Request and Merge Guidelines

- **Staging Branch:**  
  - All contributions are first merged into the staging branch.
  - **Review:** At least one review is required before merging into staging.
  - **Testing:** Changes in staging will be thoroughly tested.
- **Main Branch:**  
  - After testing on staging, changes will be merged into the main branch.
  - **Review:** Merging into main requires two reviews to ensure stability and quality.

This process ensures that our codebase remains reliable and maintainable.

---

## 6. Code Style Guidelines

To maintain a consistent codebase, please adhere to the following style guidelines:

- **Python Code:**
  - Use [flake8](https://flake8.pycqa.org/) for linting.
  - Format your code with [black](https://black.readthedocs.io/).
- **JavaScript Code:**
  - Follow the [ESLint](https://eslint.org/) guidelines.
  
Please run the linting tools before submitting your PR. If you need help setting up these tools locally, consult our public wiki.

---

## 7. Additional Guidelines

- **Documentation:**  
  Update the GitHub Wiki and in-code documentation as needed, especially when making changes that affect how the ETL tool generates code.
- **Tests:**  
  Include tests for new features or bug fixes to ensure robust functionality.
- **Commit Messages:**  
  Write clear, descriptive commit messages that explain the “what” and “why” of your changes.
- **Communication:**  
  Engage with the community via GitHub discussions or issue comments if you have any questions or need guidance.

---

## 8. Thank You!

We truly appreciate your interest in improving our ETL tool. Your contributions help make this project better for everyone. If you have any questions or need assistance, feel free to reach out via GitHub issues or our community channels.