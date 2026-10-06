
# Farm Package Example

This repository is a small demonstration of working with classes, inheritance, and importing Python3 libraries in a modular structure. It is also a safe place to practise Git. It features a `Farm` package that integrates animals, crops, and equipment, and shows the following concepts:

- Class inheritance
- Passing functions (and callable objects) as values
- Handling exceptions
- Modular code organization

**New here?** Get it running with the steps below, then:

- [Adding to the Farm](docs/ADDING_TO_THE_FARM.md): how to add your own animals, crops, equipment and crop tasks, with worked examples and exercises.
- [Git Guide](docs/GIT_GUIDE.md): branching, committing, exploring history, undoing mistakes, pull requests and merge conflicts, all using this project.

## Getting started

You need **Python 3.9 or newer** and **Git**. Check what you have:

```
python3 --version
git --version
```

> **Windows:** in these instructions, type `py` instead of `python3` if `python3` isn't found.

This project uses libraries that aren't part of a normal Python3 install, so we install them into a *virtual environment* (venv). That's a private folder of libraries for this project only, so it can't clash with anything else on your computer.

1. Get the code:
```
git clone https://github.com/rob-c/farm.git
cd farm
```

2. Create a virtual env inside the project:
```
python3 -m venv env
```

You can use any folder name, but `env` is already listed in this project's `.gitignore`, so Git won't try to commit it.

3. Activate the virtual env:

macOS / Linux:
```
source ./env/bin/activate
(env) > _
```

Windows (PowerShell):
```
.\env\Scripts\activate
```

> If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

Your prompt now starts with `(env)`, which tells you the venv is active.

4. Install the libraries this project needs into the virtual env:
```
(env) > python3 -m pip install -r requirements.txt
```

5. Run the project:
```
(env) > python3 main.py
```

You should see output like the [example output](#example-output) below. If you see `ModuleNotFoundError: No module named 'cowsay'`, the venv is not active (step 3) or the libraries aren't installed (step 4).

6. Leave the virtual env when you're finished:
```
(env) > deactivate
```

Next time, you only need steps 3 and 5.

## Directory Structure

```
.
├── animals
│   ├── base_animal.py
│   ├── chicken.py
│   ├── cow.py
│   ├── dog.py
│   ├── sheep.py
│   └── __init__.py
├── crops
│   ├── corn.py
│   ├── crop.py
│   ├── crop_tasks.py
│   ├── potato.py
│   ├── __init__.py
│   ├── rice.py
│   └── wheat.py
├── docs
│   ├── ADDING_TO_THE_FARM.md
│   └── GIT_GUIDE.md
├── equipment
│   ├── equipment.py
│   ├── faulty_equipment.py
│   ├── sprinkler.py
│   └── __init__.py
├── farm.py
├── __init__.py
├── main.py
├── Readme.md
└── requirements.txt
```

## Key Components

### Animals

- `Dog`, `Cow`, `Chicken` and `Sheep` inherit from a `BaseAnimal` class and implement the `make_noise` method to produce unique sounds.

### Crops

- The `Crop` base class is extended by specific crop types such as `Corn`, `Wheat`, `Rice` and `Potato`. Each one passes its name to `Crop` with `super().__init__(...)`.
- Crop tasks (`WaterCrop`, `FertilizeCrop`, `HarvestCrop`) are *callable objects*. They are classes with a `__call__` method, so an instance can be used like a function and applied to every crop.

### Equipment

- `Equipment` is the general case. `Sprinkler` extends it with an extra setting, and `FaultyEquipment` overrides `operate()` to raise an exception.
- The farm catches those exceptions so one broken machine doesn't stop the others.

## Features

1. **Animal Management**
   - Add animals to the farm and collect their noises with the `run_farm` method.

2. **Crop Management**
   - Add crops to the farm and apply crop tasks (watering, fertilizing, harvesting) to all of them.

3. **Equipment Operation**
   - Operate all equipment on the farm, handling exceptions for faulty equipment.

4. **Passing Functions as Values**
   - `Farm.apply_to_crops` accepts any callable, whether a crop-task object or a plain function, and calls it on each crop.

## Example Output

```
 ____________________________
< Welcome to the Python Farm >
 ----------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
Running Farm:

Applying water to crops:
corn received 10 liters of water.
wheat received 10 liters of water.
rice received 10 liters of water.
potato received 10 liters of water.

Applying fertilizer to crops:
corn was fertilized with 5 kg of Nitrogen.
wheat was fertilized with 5 kg of Nitrogen.
rice was fertilized with 5 kg of Nitrogen.
potato was fertilized with 5 kg of Nitrogen.

Harvesting crops:
2 tonnes of corn were harvested.
2 tonnes of wheat were harvested.
2 tonnes of rice were harvested.
2 tonnes of potato were harvested.

Animal noises:
Buddy says Woof!
Bessie says Moo!
Clucky says Cluck!
Shaun says Baa!
Goodbye!

Crops being grown:
The corn crop is growing.
The wheat crop is growing.
The rice crop is growing.
The potato crop is growing.

Crops need:
corn crop needs 2 litres water.
wheat crop needs 3 litres water.
rice crop needs 4 litres water.
potato crop needs 1 litre water.

Operating equipment:
The Tractor is operating.
The Plow is operating.
The Sprinkler is spraying 20 litres per minute.
Error operating Old Harvester: Old Harvester has malfunctioned!
```

The welcome banner may appear in rainbow colours, depending on your terminal.

## Learning Objectives

This repository is ideal for beginners learning about:
- Class-based object-oriented programming in Python
- Modular code organization
- Passing functions and callable objects as values
- Handling exceptions gracefully in Python
- The everyday Git workflow: branches, commits, history and pull requests

When you're ready to make it your own, head to [Adding to the Farm](docs/ADDING_TO_THE_FARM.md).
