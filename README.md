# Coderr-Backend

## Overview

This project is a Django REST Framework backend for a platform where customers can view, order, and review offers from business partners.  
It includes modules for offers (`offers_app`), orders (`orders_app`), and reviews (`reviews_app`).

## Features

- **Offers:** Business partners can create offers with various details.
- **Orders:** Customers can place orders based on offer details.
- **Reviews:** Customers can review business partners after completing an order.
- **Roles:** Distinction between customers and business partners.
- **Permissions:** Only authorized users can perform certain actions.

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

## API Endpoints (Excerpt)

### Offers (`offers_app`)
- `GET /api/offers/`  
  List all offers (with filtering and sorting options).
- `POST /api/offers/`  
  Create a new offer (business users only).
- `GET /api/offers/<id>/`  
  Retrieve a single offer (without user details).
- `GET /api/offerdetails/<id>/`  
  Retrieve a single offer detail.

### Orders (`orders_app`)
- `GET /api/orders/`  
  All orders where the logged-in user is either the customer or the business partner.
- `POST /api/orders/`  
  Create a new order based on an offer detail (`offer_detail_id` in the body).
- `PATCH /api/orders/<id>/`  
  Change the status of an order (business users only).

### Reviews (`reviews_app`)
- `GET /api/reviews/`  
  List reviews with filtering and sorting (`business_user_id`, `reviewer_id`, `ordering`).
- `POST /api/reviews/`  
  Create a new review (customers only, one review per business profile).
- `PATCH /api/reviews/<id>/`  
  Only `rating` and `description` can be changed (by the creator only).

## Roles & Permissions

- **Customer:** Can place orders and write reviews.
- **Business partner:** Can create offers and manage orders.
- **Staff:** Can view and manage all data (optional).

## Notes

- Authentication is required for all endpoints.
- User models are referenced via `settings.AUTH_USER_MODEL` and support custom user models.
- The main permissions are defined in each app under `api/permissions.py`.

## Development

- Django 4.x+
- Django REST Framework
- Python 3.10+

## License

MIT License
