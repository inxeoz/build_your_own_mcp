Let's start with simple tools like **telling the current time** and **a basic calculator**. We'll go step by step.  

---

## **📌 Step 1: Install Ollama**
If you haven’t installed **Ollama**, do it first:

```sh
pip install ollama
```

---

## **📌 Step 2: Create a Modelfile**
This tells **Ollama** how to respond when using tools.

1️⃣ Open a terminal and create a **Modelfile**:

```sh
nano Modelfile
```

2️⃣ Add the following content:

```modelfile
FROM mistral
SYSTEM "You can use two tools: 
1. To tell the time, return {\"tool\": \"get_time\"}. 
2. To calculate, return {\"tool\": \"calculator\", \"data\": {\"expression\": \"2+2\"}}."
```

3️⃣ Save and exit (**CTRL + X → Y → ENTER**).

---

## **📌 Step 3: Create the Model**
Run this command to create the **custom model**:

```sh
ollama create mymodel -f Modelfile
```

This sets up a local AI model named `mymodel`.

---

## **📌 Step 4: Write the Python Script**
Now, let’s write a Python script that will **process Ollama's responses and execute the tools**.

1️⃣ Create a new Python file:

```sh
nano chatbot.py
```

2️⃣ Add this code:

```python
import ollama
import json
import datetime

# Function to get current time
def get_time():
    return datetime.datetime.now().strftime("⏰ The current time is %H:%M:%S")

# Function to perform calculations
def calculator(expression):
    try:
        result = eval(expression)  # Be careful! Use safer eval alternatives in real apps.
        return f"🧮 The result of {expression} is {result}"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Function to process the model's response
def process_response(response):
    try:
        response_json = json.loads(response)
        tool = response_json.get("tool")
        data = response_json.get("data", {})

        if tool == "get_time":
            return get_time()
        elif tool == "calculator":
            return calculator(data.get("expression", ""))
        else:
            return "⚠️ Unknown tool request."
    except json.JSONDecodeError:
        return response  # Regular AI response

# Chat loop
while True:
    user_input = input("You: ")

    # Ask Ollama for a response
    model_response = ollama.chat(model="mymodel", messages=[{"role": "user", "content": user_input}])

    # Process response
    tool_output = process_response(model_response['message']['content'])
    print(f"🤖 Bot: {tool_output}")
```

---

## **📌 Step 5: Run the Chatbot**
Save and exit (**CTRL + X → Y → ENTER**), then run:

```sh
python chatbot.py
```

---

## **📌 Step 6: Test the Chatbot**
Try asking:

### **1️⃣ Ask for the current time**
```
You: What time is it?
🤖 Bot: ⏰ The current time is 14:35:22
```

### **2️⃣ Perform a calculation**
```
You: What is 12 * 8 + 5?
🤖 Bot: 🧮 The result of 12 * 8 + 5 is 101
```

---

## **🎯 Next Steps**
✅ **Add more tools** (like getting the date, weather, or a simple to-do list).  
✅ **Use a web interface** instead of a terminal.  
✅ **Improve error handling** for safer calculations.  

Would you like me to add **memory**, so it remembers past calculations? 😊
