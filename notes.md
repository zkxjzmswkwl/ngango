## Parsing comments

Working idea is for the format to be something similar to this:

```python
class MemberViewSet(ModelViewSet):
    """
    @ngango {
        service: Members,
        actions: {
            list,
            create,
            retrieve,
            update,
            destroy
        }
    }
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
```

`service` is included because, well, why not? At least that was my logic at the time. I'm now thinking that it might not be necessary. But unsure.

Actions are indeed necessary, barring the introduction of a much deeper contextual evaluation of the project as a whole.

Identifying the comment within a view via ast, the hierarchy would be:

- ClassDef
- body
- Expr
- Expr.value

At which point we're giving the contents of the comment as a string. Which means I need to implement a way to parse the format above. 
