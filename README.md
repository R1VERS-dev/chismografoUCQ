# API de Libros 

API sencilla para manejar libros en una biblioteca. Permite agregar, listar, eliminar y gestionar préstamos de libros, así como obtener una cita de un autor de manera externa.

---

## Endpoints

### GET `/books`
Obtiene una lista de todos los libros disponibles.

#### Respuesta de ejemplo:
```json
[
  {
    "id": 1,
    "title": "Cien Años de Soledad",
    "author": "Gabriel García Márquez",
    "quantity": 3
  },
  {
    "id": 2,
    "title": "1984",
    "author": "George Orwell",
    "quantity": 5
  }
]
```

### POST `/books`
Agrega un nuevo libro al inventario.

#### Body (JSON):
```json

{
  "title": "Fahrenheit 451",
  "author": "Ray Bradbury",
  "quantity": 4
}

```

#### DELETE /books/:id
Elimina un libro por su ID.

Ejemplo:
```bash

DELETE /books/3

```

#### GET /quote/:id
Obtiene una cita famosa del autor del libro con el ID especificado.
Este endpoint consume una API externa para obtener la frase.

Ejemplo:
```http

GET /quote/2

```

Respuesta de ejemplo:
```json

{
  "author": "George Orwell",
  "quote": "Big Brother is watching you."
}

```

#### PUT /checkout/:id
Marca el libro con el ID dado como prestado (reduce la cantidad disponible en 1).

Ejemplo:
```http

PUT /checkout/1

```

#### PUT /return/:id
Marca el libro con el ID dado como prestado (reduce la cantidad disponible en 1).

Ejemplo:
```http

PUT /return/1

```

## Notas
- Los IDs de los libros deben ser enteros únicos.
- Si la cantidad del libro llega a 0, no se podrá hacer checkout hasta que se retorne uno o se aumente la cantidad.
- El endpoint de quote se basa en el autor del libro, no directamente en el ID del autor.
