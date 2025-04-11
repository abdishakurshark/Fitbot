def calculate_bmi(weight_kg, height_m):
    """
    Calculate BMI using weight in kg and height in meters.
    Formula: BMI = weight (kg) / (height (m) ^ 2)
    """
    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive values")
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi):
    """
    Classify BMI into categories based on WHO standards.
    Returns category and health risk information.
    """
    if bmi < 18.5:
        return "Underweight", "Possible nutritional deficiency and osteoporosis"
    elif 18.5 <= bmi < 25:
        return "Normal", "Low risk (healthy range)"
    elif 25 <= bmi < 30:
        return "Overweight", "Moderate risk of developing heart disease, high blood pressure, stroke, diabetes"
    else:
        return "Obese", "High risk of developing heart disease, high blood pressure, stroke, diabetes"

%%writefile recommender.py
# Sample workout routines for different BMI categories and goals
WORKOUT_PLANS = {
    "Underweight": {
        "default": {
            "description": "Muscle building and strength training",
            "routine": [
                "Strength training 3-4 times/week (focus on compound movements)",
                "Moderate cardio 2-3 times/week (20-30 minutes)",
                "Include rest days for muscle recovery"
            ],
            "rationale": "Focuses on building muscle mass while maintaining cardiovascular health"
        },
        "Gain Muscle": {
            "description": "Intensive muscle building program",
            "routine": [
                "Strength training 4-5 times/week (heavy weights, low reps)",
                "Limited cardio (1-2 times/week for 15-20 minutes)",
                "Focus on progressive overload"
            ],
            "rationale": "Maximizes muscle growth by prioritizing strength training and minimizing calorie burn from cardio"
        }
    },
    "Normal": {
        "default": {
            "description": "Balanced fitness maintenance",
            "routine": [
                "Strength training 3 times/week (full body workouts)",
                "Cardio 2-3 times/week (30-45 minutes)",
                "Flexibility exercises (yoga or stretching) 2 times/week"
            ],
            "rationale": "Maintains overall fitness with balanced strength, cardio, and flexibility"
        },
        "Lose Weight": {
            "description": "Fat loss and toning",
            "routine": [
                "HIIT workouts 3 times/week",
                "Strength training 2 times/week (circuit training)",
                "Moderate cardio 2 times/week (30-45 minutes)"
            ],
            "rationale": "Increases calorie burn while preserving muscle mass"
        },
        "Gain Muscle": {
            "description": "Lean muscle building",
            "routine": [
                "Strength training 4 times/week (split routine)",
                "Moderate cardio 1-2 times/week (20-30 minutes)",
                "Focus on progressive overload"
            ],
            "rationale": "Builds muscle while maintaining cardiovascular health"
        }
    },
    "Overweight": {
        "default": {
            "description": "Fat burning and cardiovascular health",
            "routine": [
                "Cardio 4-5 times/week (30-45 minutes)",
                "Strength training 2-3 times/week (full body, moderate weights)",
                "Low-impact activities (walking, swimming) on rest days"
            ],
            "rationale": "Focuses on burning calories while maintaining muscle mass"
        },
        "Lose Weight": {
            "description": "Intensive fat loss program",
            "routine": [
                "HIIT workouts 3 times/week",
                "Steady-state cardio 3 times/week (45-60 minutes)",
                "Strength training 2 times/week (circuit training)"
            ],
            "rationale": "Maximizes calorie burn while preserving muscle mass"
        }
    },
    "Obese": {
        "default": {
            "description": "Low-impact fat burning and mobility",
            "routine": [
                "Low-impact cardio 5 times/week (walking, swimming, cycling - 30-45 minutes)",
                "Strength training 2 times/week (light weights, higher reps)",
                "Stretching daily to improve mobility"
            ],
            "rationale": "Focuses on sustainable calorie burn while minimizing joint stress"
        },
        "Lose Weight": {
            "description": "Sustainable weight loss program",
            "routine": [
                "Daily low-impact cardio (30-60 minutes)",
                "Strength training 2 times/week (bodyweight or light weights)",
                "Gradual progression in intensity"
            ],
            "rationale": "Provides consistent calorie burn while being safe for joints"
        }
    }
}

# Sample meal plans for different BMI categories and goals
MEAL_PLANS = {
    "Underweight": {
        "default": {
            "description": "High-calorie, nutrient-dense meals",
            "meals": [
                "Breakfast: Whole grain toast with avocado and eggs + smoothie with banana, peanut butter, and milk",
                "Snack: Greek yogurt with granola and honey",
                "Lunch: Grilled chicken with quinoa and roasted vegetables",
                "Snack: Handful of nuts and dried fruits",
                "Dinner: Salmon with sweet potato and steamed greens",
                "Before bed: Cottage cheese with berries"
            ],
            "rationale": "Provides calorie surplus with balanced macronutrients for healthy weight gain"
        },
        "Gain Muscle": {
            "description": "High-protein, calorie-dense meals",
            "meals": [
                "Breakfast: Oatmeal with protein powder, nuts, and banana",
                "Snack: Hard-boiled eggs and whole grain crackers",
                "Lunch: Lean beef with brown rice and mixed vegetables",
                "Snack: Protein shake with milk and peanut butter",
                "Dinner: Grilled chicken with pasta and pesto sauce",
                "Before bed: Casein protein pudding"
            ],
            "rationale": "Maximizes protein intake for muscle synthesis with adequate calories"
        }
    },
    "Normal": {
        "default": {
            "description": "Balanced, nutritious meals",
            "meals": [
                "Breakfast: Greek yogurt with berries and granola",
                "Snack: Apple with almond butter",
                "Lunch: Grilled chicken salad with mixed greens and olive oil dressing",
                "Snack: Hummus with vegetable sticks",
                "Dinner: Baked fish with quinoa and steamed vegetables",
                "Dessert: Dark chocolate (small portion)"
            ],
            "rationale": "Maintains health with balanced macronutrients and micronutrients"
        },
        "Lose Weight": {
            "description": "Low-calorie, high-protein meals",
            "meals": [
                "Breakfast: Scrambled eggs with spinach and whole grain toast",
                "Snack: Protein shake with almond milk",
                "Lunch: Turkey wrap with whole wheat tortilla and vegetables",
                "Snack: Cottage cheese with cucumber slices",
                "Dinner: Grilled shrimp with zucchini noodles and pesto",
                "Dessert: Sugar-free gelatin"
            ],
            "rationale": "Creates calorie deficit while maintaining protein intake to preserve muscle"
        },
        "Gain Muscle": {
            "description": "High-protein, moderate-carb meals",
            "meals": [
                "Breakfast: Protein pancakes with sugar-free syrup",
                "Snack: Tuna salad with whole grain crackers",
                "Lunch: Grilled chicken with brown rice and broccoli",
                "Snack: Protein bar and banana",
                "Dinner: Lean steak with roasted potatoes and asparagus",
                "Before bed: Casein protein shake"
            ],
            "rationale": "Supports muscle growth with adequate protein and energy from carbs"
        }
    },
    "Overweight": {
        "default": {
            "description": "Low-carb, high-protein meals",
            "meals": [
                "Breakfast: Vegetable omelette with avocado",
                "Snack: Handful of almonds",
                "Lunch: Grilled chicken Caesar salad (light dressing)",
                "Snack: Greek yogurt with chia seeds",
                "Dinner: Baked salmon with roasted vegetables",
                "Dessert: Berries with whipped cream"
            ],
            "rationale": "Reduces calorie intake while maintaining satiety and protein intake"
        },
        "Lose Weight": {
            "description": "Calorie-controlled, nutrient-dense meals",
            "meals": [
                "Breakfast: Protein smoothie with spinach and almond milk",
                "Snack: Hard-boiled egg and celery sticks",
                "Lunch: Turkey burger (no bun) with side salad",
                "Snack: Protein shake with water",
                "Dinner: Baked cod with roasted Brussels sprouts",
                "Dessert: Sugar-free popsicle"
            ],
            "rationale": "Creates significant calorie deficit while maintaining protein to preserve muscle"
        }
    },
    "Obese": {
        "default": {
            "description": "Portion-controlled, balanced meals",
            "meals": [
                "Breakfast: Scrambled eggs with sautéed vegetables",
                "Snack: Small apple with teaspoon of peanut butter",
                "Lunch: Grilled chicken with steamed vegetables",
                "Snack: Protein shake with water",
                "Dinner: Baked fish with mashed cauliflower",
                "Dessert: Herbal tea"
            ],
            "rationale": "Focuses on portion control while providing balanced nutrition"
        },
        "Lose Weight": {
            "description": "Strict calorie control with high protein",
            "meals": [
                "Breakfast: Egg white omelette with vegetables",
                "Snack: Protein shake with water",
                "Lunch: Grilled chicken breast with steamed broccoli",
                "Snack: Cucumber slices with hummus",
                "Dinner: Baked white fish with asparagus",
                "Dessert: Herbal tea"
            ],
            "rationale": "Maximizes weight loss while maintaining essential nutrients"
        }
    }
}

def get_workout_recommendation(bmi_category, goal=None):
    """Get workout recommendation based on BMI category and optional goal"""
    category_plans = WORKOUT_PLANS.get(bmi_category, {})
    
    if goal and goal in category_plans:
        return category_plans[goal]
    elif "default" in category_plans:
        return category_plans["default"]
    else:
        return {
            "description": "General fitness routine",
            "routine": ["Cardio 3 times/week", "Strength training 2 times/week"],
            "rationale": "Balanced routine for overall health"
        }

def get_meal_recommendation(bmi_category, goal=None):
    """Get meal recommendation based on BMI category and optional goal"""
    category_plans = MEAL_PLANS.get(bmi_category, {})
    
    if goal and goal in category_plans:
        return category_plans[goal]
    elif "default" in category_plans:
        return category_plans["default"]
    else:
        return {
            "description": "Balanced nutrition plan",
            "meals": [
                "Breakfast: Whole grain cereal with milk",
                "Lunch: Grilled chicken with vegetables",
                "Dinner: Fish with quinoa",
                "Snacks: Fruits and nuts"
            ],
            "rationale": "Provides balanced nutrition for general health"
        }

%%writefile app.py
import streamlit as st
from bmi import calculate_bmi, classify_bmi
from workout import get_workout_recommendation, get_meal_recommendation

# Configure Streamlit page
st.set_page_config(
    page_title="FitBot - Your AI Fitness Assistant",
    page_icon="💪",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        .highlight {
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        .recommendation-box {
            border-left: 4px solid #4CAF50;
            padding: 10px;
            margin: 10px 0;
            background-color: #f9f9f9;
        }
    </style>
""", unsafe_allow_html=True)

# App header
st.title("💪 FitBot - Your AI Fitness Assistant")
st.markdown("""
    Welcome to FitBot! I'll help you with personalized fitness recommendations based on your BMI.
    Let's get started by calculating your BMI.
""")

# User input section
with st.form("user_input"):
    st.subheader("Your Body Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
    
    with col2:
        height = st.number_input("Height (m)", min_value=1.2, max_value=2.5, value=1.75, step=0.01)
    
    goal = st.radio("Select your primary goal (optional):", 
                   ["Just analyze my BMI", "Lose Weight", "Gain Muscle"], 
                   index=0)
    
    submitted = st.form_submit_button("Calculate BMI & Get Recommendations")

# Process and display results
if submitted:
    # Calculate BMI
    try:
        bmi = calculate_bmi(weight, height)
        category, risk = classify_bmi(bmi)
        
        # Display BMI results
        st.subheader("Your BMI Results")
        st.markdown(f"""
            <div class="highlight">
                <p class="big-font">BMI: {bmi:.1f}</p>
                <p><strong>Category:</strong> {category}</p>
                <p><strong>Health Risk:</strong> {risk}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Determine goal for recommendations
        user_goal = None if goal == "Just analyze my BMI" else goal.split()[0]
        
        # Get and display workout recommendations
        st.subheader("🏋️‍♂️ Workout Recommendations")
        workout = get_workout_recommendation(category, user_goal)
        
        st.markdown(f"""
            <div class="recommendation-box">
                <p><strong>{workout['description']}</strong></p>
                <ul>
                    {''.join([f'<li>{item}</li>' for item in workout['routine']])}
                </ul>
                <p><em>Why this works for you:</em> {workout['rationale']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Get and display meal recommendations
        st.subheader("🍽️ Meal Plan Recommendations")
        meals = get_meal_recommendation(category, user_goal)
        
        st.markdown(f"""
            <div class="recommendation-box">
                <p><strong>{meals['description']}</strong></p>
                <ul>
                    {''.join([f'<li>{item}</li>' for item in meals['meals']])}
                </ul>
                <p><em>Why this works for you:</em> {meals['rationale']}</p>
            </div>
        """, unsafe_allow_html=True)
        
    except ValueError as e:
        st.error(f"Error: {str(e)} Please enter valid height and weight values.")

# Run the app using ngrok
from pyngrok import ngrok
import streamlit as st

# Setup ngrok tunnel
public_url = ngrok.connect(port='8501')
st.write(f"Public URL: {public_url}")

# Run Streamlit
!streamlit run app.py
