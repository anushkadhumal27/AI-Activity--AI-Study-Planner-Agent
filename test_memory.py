from memory import save_memory, load_memory


data = {
    "name": "Anushka",
    "subjects": [
        "DSA",
        "Java",
        "DBMS"
    ],
    "days": 7,
    "hours_per_day": 3
}


save_memory(data)

print("Memory saved!")

loaded_data = load_memory()

print("Memory loaded:")
print(loaded_data)