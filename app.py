import requests
from flask import Flask, render_template, request as req

app = Flask(__name__)

# Default text
default_text = '''Artificial Intelligence (AI) is at the forefront of technological advancement, transforming the way we live, work, and interact with the world. Its importance cannot be overstated, as it drives innovation across various domains, from healthcare to transportation and beyond.
In healthcare, AI has revolutionized diagnosis and treatment. Machine learning algorithms analyze extensive medical data to detect diseases at an early stage, improving patient outcomes and reducing medical errors. Additionally, AI-powered surgical robots perform precise and minimally invasive procedures, enhancing the quality of healthcare.
AI's impact extends into industries and businesses. Automation and predictive analytics driven by AI streamline manufacturing and logistics, increasing efficiency and reducing costs. In marketing, AI-driven tools enhance customer targeting and personalization, ultimately driving growth. Moreover, AI is a catalyst for innovation, creating new industries and jobs while contributing to economic growth.
However, as AI continues to advance, ethical considerations are paramount. Privacy concerns arise from data collection and surveillance enabled by AI, requiring robust data protection regulations. Addressing bias in algorithms is essential to ensure fairness and equity in AI applications.The future of AI is bright and promising. Researchers are working on more advanced AI models with reasoning capabilities, pushing the boundaries of what AI can achieve. In the coming years, AI will play a pivotal role in addressing global challenges, from climate change to healthcare accessibility, making it an indispensable tool for innovation and problem-solving.
In summary, Artificial Intelligence is of profound importance in our contemporary world, driving positive change across healthcare, industries, and beyond. While ethical concerns must be addressed, AI's potential for innovation and its role in solving global challenges cannot be underestimated. Its impact on society will continue to be transformative, shaping the way we work, live, and interact in the years to come.'''

@app.route("/", methods=["GET", "POST"])
def Index():
    #user_input = default_text  # Set the default text initially
    if req.method == 'POST':
        user_input = req.form.get("data", default_text)  # Get user input or use default if input is empty
    else:
        user_input=default_text
    return render_template("index.html", result="", user_input=user_input)

@app.route("/Summarize", methods=["POST"])
def Summarize():
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    data = req.form["data"]
    maxL = 500  # Change this to your desired max length
    minL = maxL // 4

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    try:
        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })[0]
        result = output["summary_text"]
    except KeyError:
        result = "You didn't enter text"

    return render_template("index.html", result=result, user_input=data)

if __name__ == '__main__':
    app.debug = True
    app.run()
