# Finance
CS50 Finance
Implement a website via which users can “buy” and “sell” stocks, a la the below.</br>
Integrate IEX to obtain real time stock prices.</br>
Allow users to create an account.</br>
Allow users to buy and sell stocks.</br>
Allows users to check cash balance and stock portfolio.</br>
Provide the ability to upload funds to an account.</br>


# Finance

A full-stack web application that lets users simulate buying, selling, and managing a real-time stock portfolio using live market data provided by the **IEX Cloud API** (or CS50's finance API proxy).

This project was completed as part of Harvard University's **CS50x: Introduction to Computer Science** (Week 9 - Web Development).

---

## 📌 Project Overview

**Finance** allows users to log in, track real-time stock prices, purchase shares using virtual currency, sell shares from their portfolio, and view a complete history of all transactions. 

Each new user starts with a virtual balance of **$10,000.00**.

---

## ✨ Features

- **User Authentication:** Secure registration, login, and logout functionality with hashed password storage.
- **Portfolio Dashboard (`/`):** View total portfolio value, cash balance, current holdings, share counts, and real-time stock valuations.
- **Quote Stock (`/quote`):** Search for real-time stock prices by ticker symbol.
- **Buy Shares (`/buy`):** Purchase shares at current market price, automatically deducting funds from the user's cash balance.
- **Sell Shares (`/sell`):** Sell owned shares at current market value, updating cash balance and holdings.
- **Transaction History (`/history`):** View an audit log of all past buy and sell orders, complete with timestamps, prices, and quantities.
- **Personalized Password Reset / Profile Settings (`/account`):** Change account password securely.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python, Flask, Jinja2 Templates
- **Database:** SQLite3 (via `cs50` SQL library)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **API Integration:** Real-time stock data fetched via HTTP requests

---


### Prerequisites

* Python 3.x installed on your machine.
* An active API key if using IEX Cloud or the CS50 Finance API endpoint.

---

### 🧠 Key Takeaways
Developing full-stack Web Applications using the Model-View-Controller (MVC) design pattern.

Handling web session state and cookie management for user authorization.

Structuring relational databases (SQL) with appropriate primary and foreign key constraints.

Validating inputs robustly on both client-side and server-side to prevent unexpected behavior and injection vulnerabilities.

Working with external RESTful APIs and parsing JSON payloads dynamically.
