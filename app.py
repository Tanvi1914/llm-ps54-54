"""Smart Recipe Generator - PS 54"""

import os
import gradio as gr
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
# Set GEMINI_API_KEY in your environment before running this application.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add your Gemini API key as an environment variable."
    )

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000)
)

print("Gemini API connected successfully!")

def generate_recipes(ingredients):
    if not ingredients or not ingredients.strip():
        return "⚠️ Please enter at least one ingredient."

    prompt = f"""
You are an intelligent recipe generation assistant.

USER'S AVAILABLE INGREDIENTS:
{ingredients}

TASK:
Generate exactly 3 different recipes using ONLY
the ingredients listed above.

STRICT INGREDIENT RULES:
1. You MUST use only the ingredients provided.
2. You may additionally use basic spices:
   salt, pepper, turmeric, chilli powder, cumin,
   coriander powder, cooking oil and water.
3. NEVER add milk, butter, cheese, coconut milk,
   garlic, ginger or any other unlisted ingredient
   unless explicitly provided by the user.
4. Do not assume ingredients are available.
5. If only a few ingredients are available,
   suggest simple variations using those ingredients.

FOR EACH RECIPE INCLUDE:

## 🍽️ Recipe 1: [Recipe Name]

A short appetizing description.

**⏱️ Preparation Time:**
**🔥 Cooking Time:**
**⭐ Difficulty:**

### 🥕 Ingredients
List ingredients with quantities.

### 👩‍🍳 Instructions
Provide numbered, easy-to-follow steps.

Use the same format for Recipe 2 and Recipe 3.

Separate each recipe using:
---

Use attractive headings and clear formatting.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=1800
            )
        )

        if response.text:
            return response.text

        return "No recipes generated. Please try again."

    except Exception as e:
        return f"Error generating recipes: {str(e)}"

import gradio as gr



custom_css = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.gradio-container {
    max-width: 1150px !important;
    margin: auto !important;
    font-family: 'DM Sans', sans-serif !important;
    background: #f7f8f2 !important;
    color: #26352c !important;
}

/* HERO */
#hero {
    background: linear-gradient(120deg, #123c2b, #28734b) !important;
    padding: 38px 32px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 22px;
}

#hero h1, #hero p, #hero .tagline {
    color: #ffffff !important;
}

/* ALL LEFT-SIDE PANELS */
.panel,
.panel > div,
.panel .wrap {
    background: #ffffff !important;
    color: #26352c !important;
    border-color: #e1e8df !important;
}

/* LEFT-SIDE HEADINGS AND TEXT */
.panel h1,
.panel h2,
.panel h3,
.panel p,
.panel label,
.panel span,
.panel strong,
.panel li {
    color: #26352c !important;
}

/* SECTION HEADINGS */
.section-heading {
    color: #17633d !important;
    font-weight: 700 !important;
}

/* INPUT LABEL */
#ingredient-box label,
#ingredient-box label span {
    color: #17633d !important;
    font-weight: 700 !important;
}

/* INPUT FIELD */
#ingredient-box textarea {
    background: #ffffff !important;
    color: #26352c !important;
    border: 1px solid #cbd8cb !important;
    border-radius: 12px !important;
}

#ingredient-box textarea::placeholder {
    color: #7b897e !important;
    opacity: 1 !important;
}

/* HELPER TEXT */
.panel .prose,
.panel .prose p,
.panel .prose strong {
    color: #37463b !important;
}

/* EXAMPLES */
.panel button,
.panel button span {
    color: #26352c !important;
}

.panel button {
    background: #f0f5ed !important;
    border: 1px solid #dce8d9 !important;
    border-radius: 9px !important;
}

.panel button:hover {
    background: #e2efdf !important;
}

/* GENERATE BUTTON */
#generate-btn {
    background: #28734b !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    min-height: 48px;
}

#generate-btn,
#generate-btn span {
    color: #ffffff !important;
}

/* CLEAR BUTTON */
#clear-btn {
    background: #edf1eb !important;
    color: #26352c !important;
    border: 1px solid #dce5d9 !important;
    border-radius: 12px !important;
    min-height: 48px;
}

/* RECIPE OUTPUT */
#recipe-output {
    background: #ffffff !important;
    border: 1px solid #e1e8df !important;
    border-radius: 18px !important;
    padding: 24px !important;
    color: #26352c !important;
}

#recipe-output,
#recipe-output * {
    color: #26352c !important;
}

#recipe-output h1,
#recipe-output h2,
#recipe-output h3,
#recipe-output h4 {
    color: #17633d !important;
    font-weight: 700 !important;
}

#recipe-output strong,
#recipe-output b {
    color: #174b31 !important;
}

#recipe-output p,
#recipe-output li {
    color: #37463b !important;
    line-height: 1.7 !important;
}

/* FOOTER */
#footer {
    text-align: center;
    color: #68786c !important;
    font-size: 13px;
    padding: 18px;
}

footer {
    display: none !important;
}

/* Keep recipe output aligned at the top */
#recipe-output {
    margin-top: 0 !important;
    min-height: 350px !important;
    height: auto !important;
    align-self: flex-start !important;
}

/* Prevent columns from stretching their contents */
.gradio-container .row {
    align-items: flex-start !important;
}

/* Remove unnecessary top spacing */
#recipe-output > div {
    margin-top: 0 !important;
}


/* RECIPE SECTION HEADING */
#recipe-heading {
    color: #174b31 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
}

/* MAIN RECIPE CONTAINER */
#recipe-output {
    background: #ffffff !important;
    border: 1px solid #e0e9df !important;
    border-radius: 20px !important;
    padding: 28px !important;
    min-height: 350px !important;
    box-shadow: 0 5px 20px rgba(27, 73, 45, 0.06) !important;
}

/* RECIPE TITLES */
#recipe-output h2 {
    color: #17633d !important;
    font-size: 23px !important;
    font-weight: 800 !important;
    padding: 15px 18px !important;
    background: #edf6ed !important;
    border-left: 5px solid #28734b !important;
    border-radius: 10px !important;
    margin-top: 24px !important;
    margin-bottom: 18px !important;
}

/* SUBHEADINGS */
#recipe-output h3 {
    color: #246343 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    margin-top: 20px !important;
}

/* DESCRIPTION AND BODY */
#recipe-output p {
    color: #46564a !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
}

/* INGREDIENTS AND INSTRUCTIONS */
#recipe-output ul,
#recipe-output ol {
    padding-left: 25px !important;
    margin-top: 10px !important;
}

#recipe-output li {
    color: #37463b !important;
    font-size: 14px !important;
    line-height: 1.9 !important;
    padding-left: 5px !important;
}

/* IMPORTANT LABELS */
#recipe-output strong {
    color: #174b31 !important;
    font-weight: 700 !important;
}

/* DIVIDERS BETWEEN RECIPES */
#recipe-output hr {
    border: none !important;
    border-top: 2px dashed #dce9dc !important;
    margin: 28px 0 !important;
}

/* RECIPE OUTPUT LINKS */
#recipe-output a {
    color: #28734b !important;
}

"""



with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="lime",
        neutral_hue="stone"
    ),
    css=custom_css
) as demo:

    # HERO SECTION
    gr.HTML("""
    <div id="hero">
        <div class="tagline">✦ AI-POWERED COOKING ASSISTANT</div>
        <h1>🍃 Smart Recipe Generator</h1>
        <p>Turn the ingredients in your kitchen into something delicious.</p>
        <p>Reduce food waste • Save money • Discover new recipes</p>
    </div>
    """)

    # MAIN CONTENT
    with gr.Row(equal_height=False, variant="default"):

        # LEFT: INGREDIENT INPUT
        with gr.Column(scale=4):
            with gr.Group(elem_classes=["panel"]):

                gr.Markdown(
                    "### 🥕 What's in your kitchen?",
                    elem_classes=["section-heading"]
                )

                gr.Markdown(
                    "Enter the ingredients you currently have. "
                    "Our AI will suggest recipes using them."
                )

                ingredients = gr.Textbox(
                    label="Available Ingredients",
                    placeholder="e.g. Potato, onion, tomato, rice...",
                    lines=5,
                    elem_id="ingredient-box"
                )

                gr.Markdown(
                    "💡 Separate ingredients with commas. "
                    "Basic spices, salt, oil and water are allowed."
                )

                generate_btn = gr.Button(
                    "✨ Generate 3 Recipes",
                    variant="primary",
                    elem_id="generate-btn"
                )

                clear_btn = gr.Button(
                    "↻ Clear Ingredients",
                    variant="secondary",
                    elem_id="clear-btn"
                )

            # QUICK EXAMPLES
            with gr.Group(elem_classes=["panel"]):
                gr.Markdown("### ⚡ Try an example")
                gr.Examples(
                    examples=[
                        ["Potato, onion, tomato"],
                        ["Rice, peas, carrot, beans"],
                        ["Paneer, capsicum, onion"],
                        ["Bread, potato, onion"],
                        ["Eggs, tomato, onion"]
                    ],
                    inputs=ingredients
                )

        # RIGHT: RECIPE RESULTS
        with gr.Column(scale=6):
            gr.Markdown(
    "## 🍽️ Discover Your Recipes",
    elem_id="recipe-heading"
)

            output = gr.Markdown(
    value="""
## 👩‍🍳 Your Kitchen, Your Recipes!

Your ingredients have the potential to become something amazing.

### What you'll get:
- 🍲 Three creative recipe suggestions
- 🥕 Ingredients with quantities
- ⏱️ Preparation and cooking time
- 📋 Easy step-by-step instructions

---

**Ready to cook?** Enter your ingredients and let AI do the planning!
""",
    elem_id="recipe-output"
)

    # FOOTER
    gr.HTML("""
    <div id="footer">
        <b>Smart Recipe Generator</b> · GenAI Mini Project · PS 54
        <br>
        Powered by Google Gemini AI
    </div>
    """)

    # BUTTON ACTIONS
    generate_btn.click(
        fn=generate_recipes,
        inputs=ingredients,
        outputs=output,
        show_progress="full"
    )

    clear_btn.click(
        fn=lambda: ("", """
### Your recipes will appear here!

Enter your ingredients to discover something delicious.
        """),
        inputs=None,
        outputs=[ingredients, output]
    )

demo.launch()
