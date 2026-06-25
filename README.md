# kpl-ticketing-system

# Event Ticketing & Booking System

This project is an implementation of an event ticketing system using **Clean Architecture** and **Domain-Driven Design (DDD)** as part of the Software Construction course at Institut Teknologi Sepuluh Nopember (ITS).

## 1. Prerequisite

Before running this project, make sure you have installed the following software:
* **Python 3.12+**
* **uv**: An extremely fast Python dependency and environment manager.
* **PostgreSQL**: The relational database required as per the project specification.
* **Visual Studio Code**: The recommended text editor with the following extensions:
    * Python (Microsoft)
    * Ruff (Astral Software) for linting and formatting.

## 2. How to Run This Project

Follow these steps for the initial setup:

1.  **Sync Dependencies**:
    Use `uv` to install all required libraries and automatically create a virtual environment:
    ```bash
    uv sync
    ```

2.  **Activate Virtual Environment**:
    * Windows: `.venv\Scripts\activate`
    * macOS/Linux: `source .venv/bin/activate`

3.  **Database Configuration**:
    You need to configure your PostgreSQL credentials before running the app. Create a `.env` file in the root directory and add the following variables:
    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_NAME=ticketing_db
    ```
    *(Make sure you have created the empty database `ticketing_db` in your PostgreSQL server).*

4.  **Run Database Migrations**:
    Apply the database schema using Alembic:
    ```bash
    alembic upgrade head
    ```

5.  **Run the Application (FastAPI)**:
    Use the following command to start the development server:
    ```bash
    uv run uvicorn src.main:app --reload
    ```

6.  **Run Unit Tests**:
    To verify domain logic:
    ```bash
    uv run pytest
    ```

---

## 3. Business Rules (BR)

The following business rules are extracted directly from the *User Stories* and *Acceptance Criteria* in the case study document:

### Event Management
* **BR1**: An event cannot be created if the end date is earlier than the start date.
* **BR2**: The maximum capacity of an event must be greater than zero.
* **BR3**: A newly created event must have a status of `Draft`.
* **BR4**: An event can only be published if it has at least one active ticket category.
* **BR5**: An event can only be published if the total ticket quota does not exceed the event's maximum capacity.
* **BR6**: An event with a `Draft` status can be changed to `Published`.
* **BR7**: An event with a `Cancelled` status cannot be published.
* **BR8**: An event with a `Published` status can be cancelled.
* **BR9**: An event with a `Completed` status cannot be cancelled.
* **BR10**: When an event is cancelled, all ticket categories can no longer be purchased.
* **BR11**: When an event is cancelled, bookings that have already been paid must be marked as `Refund Required`.

### Ticket Category
* **BR12**: The ticket price must not be less than zero.
* **BR13**: The ticket quota must be greater than zero.
* **BR14**: The ticket sales period must end before or on the event's start date.
* **BR15**: The total quota of all ticket categories must not exceed the event's maximum capacity.
* **BR16**: A ticket category can be deactivated if the event has not yet completed.
* **BR17**: Customers cannot purchase tickets from an inactive category.

### Booking & Payment
* **BR18**: A booking can only be created for an event with a `Published` status.
* **BR19**: A booking can only be created for an active ticket category.
* **BR20**: A booking can only be created within the ticket sales period.
* **BR21**: The number of tickets in a booking must be greater than zero.
* **BR22**: The number of tickets must not exceed the remaining ticket quota.
* **BR23**: A customer must not have more than one active booking for the same event.
* **BR24**: A newly created booking must have a status of `PendingPayment`.
* **BR25**: A booking must have a payment deadline.
* **BR26**: The total price must not be negative.
* **BR27**: A booking can only be paid if its status is `PendingPayment`.
* **BR28**: A booking cannot be paid if the payment deadline has passed.
* **BR29**: The payment amount must equal the total price of the booking.
* **BR30**: A booking with a `PendingPayment` status changes to `Expired` after the payment deadline has passed.
* **BR31**: A booking with a `Paid` status cannot be marked as expired.
* **BR32**: When a booking expires, the previously reserved ticket quota must be released back.

### Ticket & Check-in
* **BR33**: Check-in can only be performed for the event that corresponds to the ticket.
* **BR34**: A ticket must have an `Active` status to be checked in.
* **BR35**: A ticket that has already been checked in cannot be used again.
* **BR36**: Check-in can only be performed on the day of the event or within the permitted check-in time window.
* **BR37**: The ticket status must not change if check-in fails.

### Refund Management
* **BR38**: A refund can only be requested for a booking with a `Paid` status.
* **BR39**: A refund cannot be requested if any ticket from that booking has already been checked in.
* **BR40**: A refund can only be requested before the refund deadline.
* **BR41**: A refund can only be approved if its status is `Requested`.
* **BR42**: When a refund is approved, the associated tickets change to `Cancelled`.
* **BR43**: When a refund is approved, the associated booking changes to `Refunded`.
* **BR44**: A refund can only be rejected if its status is `Requested`.
* **BR45**: A rejection reason must be provided when rejecting a refund.
* **BR46**: When a refund is rejected, the associated booking remains at `Paid` status.
* **BR47**: A refund can only be marked as `PaidOut` if its status is `Approved`.
* **BR48**: A payment reference must be recorded when a refund is paid out (PaidOut).
* **BR49**: A refund that is already `PaidOut` cannot be approved, rejected, or cancelled again.

---

## 4. Initial Domain Model Draft

This domain model is designed based on Tactical DDD principles to maintain the consistency of business rules (Invariants).

### Aggregate Root: Event
* **Entities**: `TicketCategory`
* **Value Objects**: `DateRange`, `Money`
* **Responsibility**: Maintains the integrity of the event schedule and global ticket quota.

### Aggregate Root: Booking
* **Value Objects**: `Money`
* **Responsibility**: Manages the ticket reservation lifecycle from creation to payment or expiry.

### Aggregate Root: Ticket
* **Value Objects**: `TicketCode`
* **Responsibility**: Used by the Gate Officer for validation and the check-in process.

### Aggregate Root: Refund
* **Responsibility**: Manages the flow of refund submission, approval, and payout.

---

## 5. Ubiquitous Language Glossary

Standard terms used in this project:

| Term | Meaning |
| :--- | :--- |
| Event | An activity organized by an Event Organizer. |
| Event Organizer | A user who creates and manages events. |
| Customer | A user who orders and purchases tickets. |
| Gate Officer | A user who validates tickets during check-in. |
| Ticket Category | A type of ticket (e.g., Regular, VIP, Early Bird). |
| Quota | The maximum number of tickets available per category. |
| Booking | A temporary reservation before payment is completed. |
| Pending Payment | The status of a booking awaiting payment. |
| Paid | The status of a booking that has been fully paid. |
| Expired | The status of a booking that has passed its payment deadline. |
| Ticket | Proof of attendance created after a booking is paid. |
| Ticket Code | A unique code for ticket identification and validation. |
| Check-in | The process of validating a ticket when a participant enters the venue. |
| Refund | The process of returning money to a customer. |
| Money | A value object representing an amount and currency. |
| Sales Period | The time period during which a ticket category can be purchased. |
| Payment Deadline | The deadline for completing a booking payment. |

---

## 6. List of Implemented User Stories

Below are the 20 minimum user stories successfully implemented in this project:

**Event Management**
1. Create Event
2. Publish Event
3. Cancel Event

**Ticket Category Management**
4. Create Ticket Category
5. Disable Ticket Category

**Event Browsing and Ticket Booking**
6. View Available Events
7. View Event Details
8. Create Ticket Booking
9. Calculate Booking Total Price

**Booking Payment**
10. Pay Booking
11. Expire Booking

**Ticket and Check-in Management**
12. View Purchased Tickets
13. Check In Ticket
14. Reject Invalid Ticket Check-in

**Refund Management**
15. Request Refund
16. Approve Refund
17. Reject Refund
18. Mark Refund as Paid Out

**Reporting**
19. View Event Sales Report
20. View Event Participants

---

## 7. List of Implemented Domain Events

The system publishes the following domain events when state changes occur within aggregates:

* `EventCreated`
* `EventPublished`
* `EventCancelled`
* `TicketCategoryCreated`
* `TicketCategoryDisabled`
* `TicketReserved` (Triggered upon booking creation)
* `BookingPaid`
* `BookingExpired`
* `TicketCheckedIn`
* `RefundRequested`
* `RefundApproved`
* `RefundRejected`
* `RefundPaidOut`

---

## 8. List of Implemented Application Service Interfaces

To communicate with external systems and maintain Clean Architecture boundaries, the following interfaces are defined in the Application Layer and implemented in the Infrastructure Layer:

1. **`PaymentGateway`**: Used to process booking payments and verify transaction amounts.
2. **`NotificationService`**: Used to send notifications (e.g., Email/WhatsApp) to customers.
3. **`EventQueryService`** & **`SalesQueryService`**: CQRS query interfaces used specifically to fetch projection data such as participant lists and sales reports without loading heavy domain aggregates.

---

## 9. API Documentation & Testing

To facilitate the testing and validation of our API endpoints, we have provided a *Postman Collection* that covers all user stories implemented in this project.

### How to Run the API using Postman

1. **Import the Collection**:
   Download the `Event Ticketing System API.postman_collection.json` file from this repository and import it into your Postman application.

2. **Configure Environment**:
   * Ensure the FastAPI server is running by executing the command: `uv run uvicorn src.presentation.main:app --reload`.
   * Open the **Variables** tab within the Postman collection.
   * Ensure the `baseUrl` is set to `http://127.0.0.1:8000`.

3. **Testing Sequence**:
   To ensure data consistency and proper linkage, please execute the requests in the following order:
   * **Create Event**: Run this request first.
   * **Copy UUID**: Copy the `id` (event_id) generated in the response of the *Create Event* request.
   * **Update Variables**: Paste the `event_id` into the **Variables** tab in Postman (under the `event_id` key) so that subsequent requests (such as *Publish Event*, *Create Ticket Category*, or *Booking*) function correctly.

4. **Validation**:
   Each request has been configured to return responses that align with the *Acceptance Criteria* specified in the project's *Case Study* document.

   ---
## 10. Testing Report

For a detailed visual guide and documentation of the system's testing process, including successful API execution examples, database state, and unit test results, please refer to the official testing report PDF:

[**View Testing Report (PDF)**](https://its.id/m/TestingReport)