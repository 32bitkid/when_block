Example
=======
TODO: This is a variant of a `switch`, in C-like languages, or the `when`-expression in Kotlin. The subject expression is evaulated for the signal, and then compared to each **Case**, in order, the first one that matches will be applied to the Signal and that signal will be dispached to the `then` terminal. If no **Case** matches the **Subject** then the signal will be dispacted, unchanged, to the `else` terminal.

Properties
----------
- **Subject**: This evaulation will be matched with each **When** expression in **Cases**
- **Cases**: A collection of cases that will match against the subject
    - **When**: If this condition is equal to the subject, then **Attributes** will be applied to signal. Equality is tested using the `==` operator.
    - **Attributes**: A collection of attributes that will be applied if to the Signal
    - **Exclude existing?**: Exclude any existing attributes for this match.

Example
-------
Classification...

```
Subject: {{ $code[0:2] }}
Cases:
  - When: "SI"
    Exclude existing?: True
    Attributes:
      - Title: "mode"
        Formula: "LoadSize"
      - Title: "size"
        Forumla: "{{ int($code[2:]) }}"
  - When: "WA"
    Exclude existing?: True
    Attributes:
      - Title: "mode"
        Formula: "WaterTemperature"
      - Title: "temp"
        Forumla: "{{ int($code[2:]) }}"
  - When: "SP"
    Exclude existing?: True
    Attributes:
      - Title: "mode"
        Formula: "SpinSpeed"
      - Title: "speed"
        Forumla: "{{ int($code[2:2]) }}"
      - Title: "overdrive"
        Forumla: "{{ $code[3:] == "1" }}"
```

Commands
--------
None
