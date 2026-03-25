## **Pydantic**

When building modern Python applications—especially APIs—**data validation and parsing** become critical. This is where **Pydantic** shines.

> **Pydantic = Data validation + Parsing using Python type hints**

It ensures your data is **correct, structured, and safe**—automatically.

---

# 🔹 1. Why Pydantic?

In traditional Python:

```python
data = {"name": "Alice", "age": "25"}  # age should be int
```

You must manually validate:

- Types
- Missing fields
- Value constraints

👉 This becomes messy and error-prone.

---

## ✅ Pydantic Solves This By:

- Using **type hints**
- Automatically validating input
- Converting types when possible
- Raising clear errors when invalid

---

# 🔹 2. Basic Model

At the core of Pydantic is the **`BaseModel`**.

### 📌 Example:

```python id="f2aj7w"
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="Alice", age="25")
print(user)
```

### 🧠 Output:

```id="g0h7bb"
name='Alice' age=25
```

👉 `"25"` is automatically converted to `int`.

---

# 🔹 3. Validation Errors

If data is invalid:

```python id="8ppc0d"
User(name="Alice", age="twenty")
```

### ❗ Output:

```id="l5v4w3"
ValidationError: age is not a valid integer
```

👉 Clear, structured error messages.

---

# 🔹 4. Field Constraints

You can enforce rules:

```python id="9n66tm"
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)
```

### 🔍 Meaning:

- `gt=0` → greater than 0
- `lt=120` → less than 120

---

# 🔹 5. Default Values

```python id="v7r3rz"
class User(BaseModel):
    name: str
    age: int = 18
```

---

# 🔹 6. Optional Fields

```python id="r2n6po"
from typing import Optional

class User(BaseModel):
    name: str
    age: Optional[int] = None
```

---

# 🔹 7. Nested Models

Pydantic supports complex structures:

```python id="d8ifb6"
class Address(BaseModel):
    city: str
    zip_code: int

class User(BaseModel):
    name: str
    address: Address
```

---

# 🔹 8. Data Parsing

Works with dictionaries, JSON, etc.:

```python id="t0d5xg"
user = User.parse_obj({
    "name": "Bob",
    "age": 30
})
```

---

# 🔹 9. Serialization

Convert model → dict / JSON:

```python id="0o3h9j"
user.dict()
user.json()
```

---

# 🔹 10. Custom Validators

You can define custom rules:

```python id="a9e6lq"
from pydantic import validator

class User(BaseModel):
    name: str

    @validator('name')
    def name_must_be_capitalized(cls, v):
        if not v[0].isupper():
            raise ValueError("Must start with capital letter")
        return v
```

---

# 🔹 11. Real-World Use Case

Pydantic is widely used in:

- APIs
- Configuration management
- Data pipelines

👉 Most famously used in **FastAPI**

Example API request validation:

```python id="z4iv9x"
@app.post("/users/")
def create_user(user: User):
    return user
```

---

# 🔹 12. Advantages

### ✅ Strong Points:

- Type-safe
- Automatic parsing
- Clean error messages
- Easy to use
- Integrates with modern frameworks

---

# 🔹 13. Limitations

### ⚠️ Be aware:

- Slight performance overhead
- Learning curve for advanced validation
- Runtime validation (not compile-time)

---

# 🔹 14. Pydantic v1 vs v2 (Conceptual)

- v2 is faster (uses Rust under the hood)
- Better validation engine
- More flexible schema handling

---

# 🔹 15. Summary Table

| Feature    | Description                    |
| ---------- | ------------------------------ |
| BaseModel  | Core class for models          |
| Validation | Automatic via type hints       |
| Parsing    | Converts input data types      |
| Errors     | Structured and readable        |
| Use Case   | APIs, configs, data validation |

---

# 🔚 Final Insight

> **Pydantic turns messy input data into clean, reliable Python objects—automatically.**

In modern Python development, especially backend systems, it is almost **indispensable**.
