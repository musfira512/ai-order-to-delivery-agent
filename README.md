# AI Order-to-Delivery Agent

An AI-powered business process automation system for restaurant order management. The system uses **CrewAI, Groq LLM, Retrieval-Augmented Generation (RAG), Streamlit, and SQLite** to automate the process from customer order submission to order validation and management.

The project demonstrates how multiple AI agents can work together with traditional Python business logic and a database to automate a real-world business workflow.

---

## 1. Project Overview

The **AI Order-to-Delivery Agent** is designed for a restaurant called **Urban Bites**.

The system allows a customer to:

* Enter personal and delivery information
* Browse the restaurant menu
* Select items, sizes, and quantities
* Add items to a cart
* View subtotal, delivery charges, and total amount
* Select a payment method
* Submit the order for AI validation
* Confirm the order

After confirmation, the order is stored in a **SQLite database** and can be managed through the administration dashboard.

The main objective is to demonstrate **AI-based business process automation**, where AI agents handle understanding, knowledge retrieval, and validation while deterministic Python logic handles pricing, database operations, and workflow control.

---

# 2. Overall System Workflow

The overall process is:

```text
Customer
   ↓
Streamlit Ordering Interface
   ↓
Order Submitted
   ↓
CrewAI Agent Workflow
   │
   ├── Order Processing Agent
   │
   ├── Knowledge / RAG
   │
   └── Validation Agent
   ↓
Python Business Logic
   ↓
SQLite Database
   ↓
Admin Dashboard
   ↓
Order Status Management
```

The customer interacts only with the Streamlit interface. The AI agents operate in the background when the order is submitted.

---

# 3. Customer Ordering Procedure

### Step 1: Customer Information

The customer enters:

* Name
* Phone number
* Delivery area
* Complete delivery address
* Payment method

### Step 2: Menu Selection

The customer selects:

* Menu category
* Food item
* Size or variant where required
* Quantity

The item is then added to the cart.

### Step 3: Order Calculation

The system calculates:

```text
Subtotal
+
Delivery Fee
=
Total Amount
```

Pricing and delivery calculations are handled by Python rather than the AI model. This prevents the LLM from generating incorrect prices.

### Step 4: AI Validation

When the customer clicks **Confirm Order**, the order information is sent to the CrewAI workflow.

The AI agents verify the order information using the restaurant's business knowledge.

### Step 5: Database Storage

If the order passes validation:

* Customer information is stored
* Order information is stored
* Individual order items are stored
* Total amount is stored
* Order status is set to `CONFIRMED`

### Step 6: Order Management

The administrator can log into the Management Dashboard and manage the order status.

The workflow is:

```text
CONFIRMED
    ↓
PREPARING
    ↓
OUT_FOR_DELIVERY
    ↓
DELIVERED
```

---

# 4. AI Agents

The project uses multiple specialized agents instead of assigning the complete task to a single AI agent.

## 4.1 Order Processing Agent

### Role

The Order Processing Agent understands and extracts information from the customer's order.

### Responsibilities

It identifies:

* Customer name
* Phone number
* Delivery area
* Delivery address
* Payment method
* Ordered products
* Quantity
* Size or variant

It uses the restaurant's knowledge base to understand available products and options.

### Example

If the customer orders:

```text
2 Large BBQ Chicken Pizzas
```

the agent identifies:

```text
Product: BBQ Chicken Pizza
Quantity: 2
Size: Large
```

The agent does not invent menu items or prices.

---

# 5. Knowledge / RAG System

The system uses **Retrieval-Augmented Generation (RAG)** to provide the AI agents with restaurant-specific information.

The knowledge base contains documents such as:

```text
knowledge/
├── menu.txt
├── delivery.txt
├── policies.txt
└── faq.txt
```

These documents contain information about:

* Menu items
* Prices
* Pizza sizes
* Customizations
* Delivery areas
* Delivery charges
* Restaurant policies
* Frequently asked questions

The knowledge is retrieved when the AI agents need restaurant-specific information.

This prevents the agents from relying only on their general language-model knowledge.

---

# 6. Validation Agent

The Validation Agent receives the information extracted by the Order Processing Agent and checks whether the order is complete and valid.

It verifies:

* Products
* Quantity
* Size or variant
* Customer information
* Phone number
* Delivery area
* Delivery address
* Payment method
* Availability of requested products

The agent returns a structured JSON result.

Example:

```json
{
    "order_status": "COMPLETE",
    "items": [
        {
            "product": "BBQ Chicken Pizza",
            "quantity": 2,
            "size": "Large"
        }
    ],
    "customer_name": "Ahmed",
    "phone": "03001234567",
    "delivery_area": "Johar Town",
    "delivery_address": "Johar Town Lahore",
    "payment_method": "Cash on Delivery (COD)",
    "missing_information": []
}
```

If information is missing, the status becomes:

```text
INCOMPLETE
```

and the missing fields are identified.

---

# 7. CrewAI Workflow

The agents are organized using **CrewAI**.

The workflow uses a sequential process:

```text
Customer Order
      ↓
Order Processing Agent
      ↓
Validation Agent
      ↓
Validation Result
```

The output of the Order Processing Agent is provided as context to the Validation Agent.

This creates a controlled multi-agent workflow rather than allowing agents to work independently without coordination.

---

# 8. Role of the LLM

The project uses **Groq** as the LLM provider.

The model is:

```text
openai/gpt-oss-120b
```

The LLM is used for tasks that require natural-language understanding, such as:

* Understanding customer order information
* Extracting structured information
* Interpreting restaurant knowledge
* Identifying missing information
* Validating order details

The LLM is **not responsible for critical deterministic calculations**.

---

# 9. Deterministic Business Logic

Traditional Python logic is used where predictable and exact results are required.

For example:

### Pricing

```text
Item Price × Quantity
```

is calculated by Python.

### Delivery Fee

Delivery charges are calculated according to the configured restaurant delivery rules.

Orders of **Rs. 3,000 or more** receive free delivery within the configured delivery policy.

### Database Operations

Python handles:

* Creating customers
* Creating orders
* Adding order items
* Updating order status
* Retrieving orders

This hybrid approach combines AI flexibility with deterministic business logic.

---

# 10. Database

The project uses **SQLite** as the database.

The database contains three main tables:

### Customers

Stores:

* Customer ID
* Name
* Phone
* Address
* Creation time

### Orders

Stores:

* Order ID
* Customer ID
* Order status
* Payment method
* Total amount
* Creation time
* Last update time

### Order Items

Stores:

* Order ID
* Product name
* Quantity
* Size
* Unit price

The relationships are:

```text
Customers
    │
    └── Orders
          │
          └── Order Items
```

---

# 11. Admin Dashboard

The system includes a separate management section.

The administrator can:

* Log into the management dashboard
* View customer orders
* View order details
* View payment method
* View total amount
* View ordered items
* Update order status

The customer ordering interface and management interface are separated to keep the system organized.

---

# 12. Technology Stack

| Technology                | Purpose                        |
| ------------------------- | ------------------------------ |
| Python                    | Main programming language      |
| Streamlit                 | Web interface                  |
| CrewAI                    | Multi-agent orchestration      |
| Groq                      | LLM provider                   |
| GPT-OSS-120B              | Language model                 |
| RAG                       | Restaurant knowledge retrieval |
| Sentence Transformers     | Text embeddings                |
| SQLite                    | Database                       |
| GitHub Codespaces         | Development environment        |
| Streamlit Community Cloud | Deployment                     |

---

# 13. Project Structure

```text
ai-order-to-delivery-agent/
│
├── app.py
│
├── agents/
│   ├── order_agent.py
│   └── validation_agent.py
│
├── crews/
│   └── order_crew.py
│
├── tasks/
│   ├── order_tasks.py
│   └── validation_tasks.py
│
├── services/
│   └── order_ai.py
│
├── rag/
│   ├── knowledge.py
│   └── documents/
│
├── knowledge/
│   ├── menu.txt
│   ├── delivery.txt
│   ├── policies.txt
│   └── faq.txt
│
├── database/
│   ├── connection.py
│   ├── models.py
│   └── crud.py
│
├── data/
│   └── menu.py
│
├── utils/
│   └── pricing.py
│
├── config/
│   └── settings.py
│
├── requirements.txt
└── README.md
```

---

# 14. How the Components Work Together

The complete process can be summarized as:

```text
                  CUSTOMER
                     │
                     ▼
             STREAMLIT UI
                     │
                     ▼
              ORDER SUBMITTED
                     │
                     ▼
             CREWAI WORKFLOW
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   ORDER PROCESSING       KNOWLEDGE / RAG
       AGENT                   │
          │                    │
          └──────────┬─────────┘
                     ▼
              VALIDATION AGENT
                     │
                     ▼
             VALIDATION RESULT
                     │
                     ▼
          PYTHON BUSINESS LOGIC
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
       PRICING              SQLITE DB
                                │
                                ▼
                       ADMIN DASHBOARD
                                │
                                ▼
                       ORDER WORKFLOW
```

---

# 15. Why a Hybrid AI Architecture is Used

The system does not give complete control of the business process to the LLM.

Instead:

### AI handles

* Natural-language understanding
* Information extraction
* Knowledge retrieval
* Order validation

### Python handles

* Pricing
* Delivery fee calculation
* Database operations
* Order IDs
* Status changes
* Final order storage

This makes the system more reliable because AI is used where language understanding is useful, while deterministic code is used for operations that require exact results.

---

# 16. Running the Project

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd ai-order-to-delivery-agent
```

Create and activate the virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the Groq API key as an environment variable:

```text
GROQ_API_KEY
```

Then start the Streamlit application:

```bash
streamlit run app.py
```

---

# 17. Deployment

The application can be deployed using **Streamlit Community Cloud**.

The GitHub repository is connected to Streamlit Community Cloud, and the main application file is:

```text
app.py
```

The Groq API key is configured as a deployment secret rather than being stored directly in the source code.

---

# 18. Project Objective

The main objective of this project is to demonstrate how **AI agents can automate a real-world business process**.

Instead of using AI only as a chatbot, the system integrates AI into an actual workflow:

```text
Customer Order
      ↓
AI Understanding
      ↓
Knowledge Retrieval
      ↓
AI Validation
      ↓
Business Processing
      ↓
Database
      ↓
Order Management
```

This demonstrates the use of AI agents as components of a larger **business process automation system**.
