# Coderr-Backend

## Overview

Coderr-Backend is a Django REST Framework backend for a platform where customers can view, order, and review offers from business partners.  
It is structured into three main modules:  
- **Offers** (`offers_app`): Manage business offers and their details  
- **Orders** (`orders_app`): Customers can place orders based on offer details  
- **Reviews** (`reviews_app`): Customers can review business partners after an order

## Features

- **Role-based access:** Customers and business partners have different permissions and capabilities.
- **Custom user model:** Fully supports a custom user model via `settings.AUTH_USER_MODEL`.
- **Offer management:** Business partners can create, update, and list offers with multiple details.
- **Order workflow:** Customers can create orders from offer details; business partners manage order status.
- **Review system:** Customers can review business partners (one review per business profile).
- **Filtering & sorting:** API supports filtering and ordering for offers, orders, and reviews.
- **Statistics endpoint:** General statistics about the platform (number of reviews, average rating, etc.).

## Installation

1. **Clone the repository**
   ```bash
   git clone <REPO-URL>
   cd Coderr-Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints (Selection)

### Offers (`offers_app`)
- `GET /api/offers/`  
  List all offers (supports filtering and ordering).
- `POST /api/offers/`  
  Create a new offer (business users only).
- `GET /api/offers/<id>/`  
  Retrieve a single offer (without user details).
- `GET /api/offerdetails/<id>/`  
  Retrieve a single offer detail.

### Orders (`orders_app`)
- `GET /api/orders/`  
  List all orders where the logged-in user is either the customer or the business partner.
- `POST /api/orders/`  
  Create a new order based on an offer detail (`offer_detail_id` in the body).
- `PATCH /api/orders/<id>/`  
  Change the status of an order (business users only).

### Reviews (`reviews_app`)
- `GET /api/reviews/?business_user_id=&reviewer_id=&ordering=`  
  List reviews, filterable by business user, reviewer, and orderable by `updated_at` or `rating`.
- `POST /api/reviews/`  
  Create a new review (customers only, one review per business profile).
- `PATCH /api/reviews/<id>/`  
  Only `rating` and `description` can be changed (by the creator only).

### Statistics (`core`)
- `GET /api/base-info/`  
  Returns general statistics: review count, average rating, business profile count, offer count.

## Roles & Permissions

- **Customer:** Can place orders and write reviews.
- **Business partner:** Can create offers and manage orders.
- **Staff:** Can view and manage all data (optional).
- Permissions are enforced via custom permission classes in each app.

## Notes

- All endpoints require authentication unless otherwise noted.
- The user model is referenced via `settings.AUTH_USER_MODEL` and supports custom user models.
- Main permissions are defined in each app under `api/permissions.py`.
- The project uses Django 4.x+, Django REST Framework, and Python 3.10+.

## Development

- Python 3.10+
- Django 4.x+
- Django REST Framework
- SQLite (default, can be changed)

## License

MIT License
