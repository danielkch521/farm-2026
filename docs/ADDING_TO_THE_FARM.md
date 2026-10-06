# Adding to the Farm

This guide walks through extending the farm with your own animals, crops,
equipment and crop tasks. Every section follows the same pattern, and every
section has a **real commit in this repository** you can inspect to see
exactly what changed.

If you have not set up the project yet, follow the setup steps in the
[Readme](../Readme.md) first and check that `python3 main.py` runs.

## The pattern

Almost everything on the farm follows the same four steps:

1. **Find the base class** that describes the kind of thing you are adding.
2. **Write a subclass** of it in a new file and fill in the methods it needs.
3. **Export it** from the package's `__init__.py` so it is easy to import.
4. **Use it** in `main.py` (or `farm.py`) so it actually shows up when the
   program runs.

| You want to add... | Base class                      | New file goes in | Methods to write   | Worked example commit       |
|--------------------|---------------------------------|------------------|--------------------|-----------------------------|
| An animal          | `BaseAnimal` (`animals/base_animal.py`) | `animals/` | `make_noise()`     | "Add Sheep animal"          |
| A crop             | `Crop` (`crops/crop.py`)        | `crops/`         | `water_req()`      | "Add Potato crop"           |
| Equipment          | `Equipment` (`equipment/equipment.py`) | `equipment/` | `operate()` (optional) | "Add Sprinkler equipment" |
| A crop task        | none, it is a *callable* class  | `crops/crop_tasks.py` | `__call__()`  | "Add HarvestCrop crop task" |

## Before you start: make a branch

Do your work on a branch so you can always get back to a working
version. Pick a name that describes what you're adding:

```
git switch -c add-goat
```

The [Git guide](GIT_GUIDE.md) explains branches in more detail.

---

## Adding an animal

**Worked example:** to see exactly what adding the sheep changed, run

```
git log --oneline --grep "Sheep"
git show <the commit id it printed>
```

### 1. Create the class

Make a new file `animals/goat.py`:

```python
from .base_animal import BaseAnimal

class Goat(BaseAnimal):
    def make_noise(self):
        return f"{self.name} says Meh!"
```

There are a few things to notice:

- `from .base_animal import BaseAnimal`: the leading `.` means "from this
  same package (folder)".
- `class Goat(BaseAnimal)` means a Goat *is a* BaseAnimal. It inherits
  `__init__`, so `Goat("Gruff")` sets `self.name = "Gruff"` without you
  writing any extra code.
- `make_noise` *overrides* the version in `BaseAnimal`. The base version just
  raises `NotImplementedError`, which is how the base class says "every animal
  must provide this".

### 2. Export it

Add one line to `animals/__init__.py`:

```python
from .goat import Goat
```

`main.py` imports animals by their full path (`from animals.goat import Goat`),
so strictly this step is optional for animals. It is still good practice,
because it lets anyone write `from animals import Goat`.

### 3. Use it

In `main.py`, import it alongside the other animals:

```python
from animals.goat import Goat
```

and add one to the farm next to the others:

```python
    farm.add_animal(Goat("Gruff"))
```

### 4. Run it

```
python3 main.py
```

You should see `Gruff says Meh!` in the "Animal noises" section.

### 5. Commit it

```
git status                 # see what changed: goat.py is "untracked"
git add animals/goat.py animals/__init__.py main.py
git commit -m "Add Goat animal"
```

---

## Adding a crop

**Worked example:** `git log --oneline --grep "Potato"`, then `git show` it.

### 1. Create the class

Make `crops/carrot.py`:

```python
from .crop import Crop

class Carrot(Crop):
    def __init__(self):
        super().__init__('carrot')

    def water_req(self):
        return "2 litres"
```

Crops differ from animals in one way: the *crop itself* decides its name.
`super().__init__('carrot')` calls `Crop.__init__`, which stores the name in
`self.name`. If you forget it, the crop has no name.

`water_req()` is required. `Crop.water_needs()` calls it, and the base
version raises `NotImplementedError` if a subclass doesn't provide one.

### 2. Export it (required for crops)

Add to `crops/__init__.py`:

```python
from .carrot import Carrot
```

For crops this step is **not** optional. `main.py` uses
`from crops import *`, which imports whatever `crops/__init__.py` imports
and nothing else. If you skip this, you get:

```
NameError: name 'Carrot' is not defined
```

### 3. Use it, run it, commit it

In `main.py`:

```python
    farm.add_crop(Carrot())
```

Run `python3 main.py`. The carrot should be watered, fertilized, harvested
and grown, because `Farm` applies every task to every crop in its list. Then
commit:

```
git add crops/carrot.py crops/__init__.py main.py
git commit -m "Add Carrot crop"
```

---

## Adding equipment

There are two ways to add equipment, depending on whether you need new
*behaviour* or just a new *thing*.

### Option A: a new piece of the same kind (no new class)

If it works like ordinary equipment, just make another one in `main.py`:

```python
    farm.add_equipment(Equipment("Combine Harvester"))
```

Each `Equipment(...)` is an *object* (an instance) of the `Equipment`
*class*. You don't need a new class for every tractor.

### Option B: a new kind of equipment (new class)

**Worked example:** `git log --oneline --grep "Sprinkler"`, then `git show` it.

When it should behave differently, subclass `Equipment` and override
`operate()`. The sprinkler also takes an extra setting, so it extends
`__init__`:

```python
from .equipment import Equipment

class Sprinkler(Equipment):
    def __init__(self, name, litres_per_minute):
        super().__init__(name)                    # let Equipment set self.name
        self.litres_per_minute = litres_per_minute

    def operate(self):
        return f"The {self.name} is spraying {self.litres_per_minute} litres per minute."
```

`equipment/__init__.py` is empty, so `main.py` imports equipment by full
path:

```python
from equipment.sprinkler import Sprinkler
...
    farm.add_equipment(Sprinkler("Sprinkler", 20))
```

**Equipment that can fail:** look at `equipment/faulty_equipment.py`. Its
`operate()` raises an exception, and `Farm.operate_all_equipment()` catches
it with `try`/`except` so one broken machine doesn't stop the whole farm.
Try writing your own piece of equipment that breaks in a different way, for
example raising `ValueError("out of fuel")`.

---

## Adding a crop task

**Worked example:** `git log --oneline --grep "HarvestCrop"`, then `git show` it.

Crop tasks such as `WaterCrop`, `FertilizeCrop` and `HarvestCrop` are
*callable objects*: classes with a `__call__` method, so an instance can be
called like a function. You set them up once with their settings, then call
them on each crop:

```python
water = WaterCrop(10)      # __init__ runs: remember "10 litres"
water(corn)                # __call__ runs: "corn received 10 liters of water."
```

### 1. Add the class to `crops/crop_tasks.py`

```python
class InspectCrop:
    def __init__(self, inspector):
        self.inspector = inspector

    def __call__(self, crop):
        return f"{self.inspector} inspected the {crop.name}."
```

`crops/__init__.py` already does `from .crop_tasks import *`, so anything in
this file is exported automatically.

### 2. Use it in `farm.py`

Tasks are applied inside `Farm.run_farm()`. Create one and pass it to
`apply_to_crops`, which calls it once per crop:

```python
        inspect_functor = InspectCrop("Old MacDonald")
        ...
        msg += "\n\n"
        msg += "Inspecting crops:\n"
        msg += self.apply_to_crops(inspect_functor)
```

`apply_to_crops` doesn't care *what* you give it, as long as it can be
called with a crop. A plain function works too:

```python
def count_letters(crop):
    return f"{crop.name} has {len(crop.name)} letters."

msg += self.apply_to_crops(count_letters)
```

This idea is called *passing functions as values*, and it is used all over
Python (`sorted(key=...)`, `map(...)`, callbacks, and more).

---

## When it goes wrong

These are real error messages from making each mistake in this project.

| Mistake | What you see |
|---------|--------------|
| Typo in the class name in `main.py` | `NameError: name 'Shep' is not defined. Did you mean: 'Sheep'?` |
| Forgot to add a crop to `crops/__init__.py` | `NameError: name 'Potato' is not defined` |
| Forgot `water_req()` on a crop | `NotImplementedError: Subclasses must implement water_req method` |
| Forgot `make_noise()` on an animal | `NotImplementedError: Subclasses must implement make_noise method` |
| Forgot `super().__init__(name)` in equipment | `AttributeError: 'Sprinkler' object has no attribute 'name'` |
| Added the file but never called `farm.add_...` | No error. It just never appears in the output. |

Some tips for reading a Python error (a *traceback*):

- **Read the last line first.** It names the error and the problem.
- **Then read upwards** to find the first file that is *yours*. That's
  usually where the fix goes.
- `During handling of the above exception, another exception occurred` means
  the error happened inside an `except` block. You get exactly this if you
  forget `super().__init__` in equipment: `operate_all_equipment` catches
  the first error, then fails again trying to print `eq.name`.

If you get stuck, `git diff` shows everything you've changed since your last
commit, and `git restore <file>` puts a file back the way it was. See the
[Git guide](GIT_GUIDE.md#undoing-things).

---

## Exercises

Try these in order. Make each one on its own branch and commit it when it
works.

1. **Goat**: add a goat, following the animal section above.
2. **Carrot**: add a carrot crop with its own water needs.
3. **Combine Harvester**: add one with `Equipment(...)`, with no new class.
4. **Out-of-fuel tractor**: a new equipment class whose `operate()` raises
   `ValueError("out of fuel")`. Check that the farm keeps running.
5. **InspectCrop**: add the crop task from above and use it in `run_farm`.
6. **Loud animal**: an animal that takes an extra `volume` argument in
   `__init__` and says its noise in capitals when `volume > 5`. (Hint: look
   at how `Sprinkler` extends `__init__`.)
7. **Stretch**: give `Crop` a `harvest_tonnes()` method that each crop
   overrides, and change `HarvestCrop` to use it instead of a fixed number.
