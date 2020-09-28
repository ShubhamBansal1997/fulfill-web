# Product

!!!info
    For API overview and usages, check out [this page](0-overview.md).

## Add Product

```
POST /api/product
```

__Parameters__

Name        | Description
------------|-------------------------------------
sku         | sku of the product.
name        | name of the product.
description | description of the product.

__Request__
```json
{
  "name":"name",
  "sku":"sku",
  "description":"description"
}
```

__Response__
```json

Status: 201 Created
{
  "id":"56131531-7f21-4859-bf8e-375da4418136",
  "created_at":"2020-09-28T22:02:45.710762Z",
  "modified_at":"2020-09-28T22:02:45.710800Z",
  "name":"name",
  "sku":"sku",
  "description":"description"
}
```


## Update Product

Update the Product as per the product id

```
PUT /api/product/<pk>
```

__Parameters__

| Name       | Description                                                |
| ---------- | ---------------------------------------------------------- |
| pk         | primary key of the product |


**Request**

```json
{
  "name":"name",
  "sku":"sku",
  "description":"description"
}
```

__Response__

```json

Status: 200 Ok
{
  "id":"56131531-7f21-4859-bf8e-375da4418136",
  "created_at":"2020-09-28T22:02:45.710762Z",
  "modified_at":"2020-09-28T22:02:45.710800Z",
  "name":"name",
  "sku":"sku",
  "description":"description"
}
```


## List of the Products

Get the list of all the products

```
GET /api/product
```

__Parameters__

Name        | Description
------------|-------------------------------------
search      | (required) search key for the tables
sku         | (optional) sku value to filter
name        | (optional) name to filter
description | (optional) description to filter
page        | (optional) page number (paginated api)


__Response__
```json

Status: 200 OK
{
  "count":438836,
  "next":"http://localhost:8000/api/product?ordering=-sku&page=2",
  "previous":null,
  "results":[
    {
      "id":"54b0f9cc-d0be-4cca-9316-f7d113520abc",
      "created_at":"2020-09-28T18:21:58.858874Z",
      "modified_at":"2020-09-28T18:21:58.858885Z",
      "name":"Zachary Howard",
      "sku":"yourself-would-try",
      "description":"Question instead whole. Them even less knowledge painting open number require. Check five production never evening step."
    }
  ]
}
```


## Delete Product

Delete a single product as per the product id
```
DELETE /api/product/<pk>
```

__Parameters__

Name          | Description
--------------|-------------------------------------
pk            | id of the product


__Request__
```json
```

__Response__
```
Status: 204 No-Content
```

## Delete All Products

Delete all Products in the DB

```
DELETE /api/product/deleteall
```


__Request__
```json
```

__Response__
```
Status: 200 Ok
{
    "success": "Deleted all records."
}
```

## Products file Upload

Used to Upload data from the file

```
GET /api/file_upload
```

__Request__

Name          | Description
--------------|-------------------------------------
file          | file to be uploaded


__Response__
```json

Status: 201 Created
{
  "id":"54b0f9cc-d0be-4cca-9316-f7d113520abc",
  "created_at":"2020-09-28T18:21:58.858874Z",
  "modified_at":"2020-09-28T18:21:58.858885Z",
  "file":"test.csv",
  "task_id":"54b0-4ccaf9cc-d0be-4cca-9316-f70abc"
}
```



!!!Note
    The verification link uses the format of key `password-confirm` in `FRONTEND_URLS` dict in settings/common.
