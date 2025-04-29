# API Documentation

## Overview

This API provides a simple endpoint to create purchase records in a database. It is designed to monitor real-time purchases made on a website. The API is lightweight and focuses solely on this functionality.

## Endpoint

### Create Purchase Record

**POST** `/purchases`

#### Description

This endpoint allows the creation of a new purchase record in the database. It is intended to capture and store purchase data in real-time for monitoring purposes.

#### Request Body

The request body should contain the necessary information about the purchase. The exact structure of the payload depends on the implementation but typically includes details such as:

- **Product ID**: Identifier of the purchased product.
- **Price**: Total price of the purchase.
- **Campaign**: Identifier of the marketing campaign associated with the purchase.
- **Source**: Source from which the user arrived (e.g., website, referral).
- **Medium**: Medium through which the user interacted (e.g., email, social media).

#### Response

- **201 Created**: The purchase record was successfully created.
- **400 Bad Request**: The request body is invalid or missing required fields.
- **500 Internal Server Error**: An error occurred while processing the request.

#### Example Usage

**Request:**

```http
POST /purchases HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
    "product_id": "12345",
    "price": 49.99,
    "campaign": "summer_sale",
    "source": "website",
    "medium": "email"
}
```

**Response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "status": "ok",
    "msg": "Purchase successfully saved to database"
}
```
