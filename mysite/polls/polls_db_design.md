Polls database model using crow's foot notation (entity relationship model)

```mermaid
    erDiagram
    USER }|--O{ QUESTION : asks
    USER {
        int id
        string name
        string email
    }
    QUESTION ||--|{ CHOICE : has
    QUESTION {
        int id
        string name
        string email
    }
    CHOICE {
        int id
        int question_id
        string choice_text
        int votes
    }
```
ER diagram key:
```mermaid
    erDiagram
    zero_or_one |o--|| exactly_one : relationship
    zero_or_more }o--|{ one_or_more : relationship


```
