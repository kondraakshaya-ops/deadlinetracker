
from urllib.parse import quote

from google import genai
import streamlit as st
from datetime import date


GEMIMI_API_KEY = st.secrets["GEMINI_API_KEY"]


def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)
gemini_clinet = get_gemini_client(GEMIMI_API_KEY)
#------------------AI MODEL--------------
MODEL_NAME = "gemini-2.0-flash"


def build_whatsapp_message(task_name: str, due_date: str, priority: str, urgency: str) -> str:
    """Build the pre-filled WhatsApp message text."""
    body = (
        f"\U0001f4cc *Deadline Reminder*\n"
        f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
        f"\U0001f4dd Task: {task_name}\n"
        f"\U0001f4c5 Due Date: {due_date}\n"
        f"\U0001f525 Priority: {priority}\n"
        f"\u23f0 Status: {urgency}\n"
        f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
        f"Sent via Deadline Tracker \U0001f5d3\ufe0f"
    )
    return body


def get_whatsapp_link(phone: str, message: str) -> str:
    """Return a wa.me link with a pre-filled message for a specific number."""
    # Strip spaces, dashes; keep the + sign
    clean_phone = phone.replace(" ", "").replace("-", "")
    if clean_phone.startswith("+"):
        clean_phone = clean_phone[1:]  # wa.me doesn't want the +
    encoded = quote(message, safe="")
    return f"https://wa.me/{clean_phone}?text={encoded}"


def get_whatsapp_link_no_number(message: str) -> str:
    """Return a wa.me link with pre-filled text but NO specific number (user picks contact)."""
    encoded = quote(message, safe="")
    return f"https://wa.me/?text={encoded}"

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Deadline Tracker",
    page_icon="D",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background: #f4f7fb;
}

.main-title {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.main-title h1 {
    font-size: 42px;
    margin: 0;
}

.main-title p {
    font-size: 17px;
    margin-top: 8px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #e5e7eb;
}

.task-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border-left: 6px solid #4f46e5;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.high {
    border-left-color: #ef4444;
}

.medium {
    border-left-color: #f59e0b;
}

.low {
    border-left-color: #22c55e;
}

.overdue {
    border-left-color: #dc2626;
}

.completed {
    border-left-color: #16a34a;
}

.small {
    color: #6b7280;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STORAGE ----------------

if "deadlines" not in st.session_state:
    st.session_state.deadlines = []

if "show_extra_number" not in st.session_state:
    st.session_state.show_extra_number = {}


# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
    <h1>Deadline Tracker</h1>
    <p>Stay organized. Stay focused. Never miss an important deadline.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- CALCULATIONS ----------------

total = len(st.session_state.deadlines)

completed = 0
pending = 0
overdue = 0
due_today = 0

for item in st.session_state.deadlines:

    if item["status"] == "Completed":
        completed += 1
    else:
        pending += 1

        if item["due_date"] < date.today():
            overdue += 1

        if item["due_date"] == date.today():
            due_today += 1


if total > 0:
    progress = completed / total
else:
    progress = 0


# ---------------- DASHBOARD ----------------

st.subheader("Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Tasks", total)

with c2:
    st.metric("Pending", pending)

with c3:
    st.metric("Completed", completed)

with c4:
    st.metric("Overdue", overdue)


st.progress(
    progress,
    text="Completion progress: " + str(int(progress * 100)) + "%"
)

st.divider()


# ---------------- ADD DEADLINE ----------------

st.subheader("Add New Deadline")

with st.form("add_deadline_form"):

    col1, col2 = st.columns(2)

    with col1:

        task = st.text_input(
            "Task / Assignment",
            placeholder="Example: DBMS Assignment"
        )

        subject = st.text_input(
            "Subject",
            placeholder="Example: DBMS"
        )

        description = st.text_area(
            "Description",
            placeholder="Enter task details"
        )

    with col2:

        due_date = st.date_input(
            "Due Date",
            min_value=date.today()
        )

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )



    add_button = st.form_submit_button(
        "Add Deadline",
        use_container_width=True
    )

    if add_button:

        if task.strip() == "":
            st.error("Please enter a task.")

        elif subject.strip() == "":
            st.error("Please enter a subject.")

        else:

            new_task = {
                "task": task,
                "subject": subject,
                "description": description,
                "due_date": due_date,
                "priority": priority,
                "status": "Pending",
                "phones": []
            }

            st.session_state.deadlines.append(new_task)

            st.success("Deadline added successfully.")

            st.rerun()


st.divider()


# ---------------- SEARCH AND FILTER ----------------

st.subheader("Find Deadlines")

col1, col2, col3 = st.columns(3)

with col1:

    search = st.text_input(
        "Search",
        placeholder="Search task or subject"
    )

with col2:

    status_filter = st.selectbox(
        "Status",
        ["All", "Pending", "Completed"]
    )

with col3:

    priority_filter = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"]
    )


# ---------------- FILTER TASKS ----------------

filtered_tasks = []

for index, item in enumerate(st.session_state.deadlines):

    text = (
        item["task"] + " " + item["subject"]
    ).lower()

    if search.strip() != "":
        if search.lower() not in text:
            continue

    if status_filter != "All":
        if item["status"] != status_filter:
            continue

    if priority_filter != "All":
        if item["priority"] != priority_filter:
            continue

    filtered_tasks.append((index, item))


# ---------------- DISPLAY TASKS ----------------

st.subheader("Your Deadlines")


if len(filtered_tasks) == 0:

    st.info("No deadlines found.")

else:

    for index, item in filtered_tasks:

        task_class = item["priority"].lower()

        status_text = "Pending"

        if item["status"] == "Completed":
            task_class = "completed"
            status_text = "Completed"

        elif item["due_date"] < date.today():
            task_class = "overdue"
            status_text = "OVERDUE"

        elif item["due_date"] == date.today():
            status_text = "DUE TODAY"

        elif item["due_date"] > date.today():
            status_text = "Upcoming"


        description_text = item["description"]

        if description_text == "":
            description_text = "No description provided."


        st.markdown(
            '<div class="task-card ' + task_class + '">'
            '<h3>' + item["task"] + '</h3>'
            '<p class="small">Subject: ' + item["subject"] + '</p>'
            '<p>Due date: <b>' + str(item["due_date"]) + '</b></p>'
            '<p>Priority: <b>' + item["priority"] + '</b></p>'
            '<p>Status: <b>' + status_text + '</b></p>'
            '<p>' + description_text + '</p>'
            '</div>',
            unsafe_allow_html=True
        )


        b1, b2, b3 = st.columns(3)

        with b1:

            if item["status"] == "Pending":

                if st.button(
                    "Mark as Completed",
                    key="complete_" + str(index),
                    use_container_width=True
                ):

                    st.session_state.deadlines[index]["status"] = "Completed"

                    st.rerun()


        with b2:

            if st.button(
                "Delete",
                key="delete_" + str(index),
                use_container_width=True
            ):

                st.session_state.deadlines.pop(index)

                st.rerun()

        with b3:

            # Build urgency string
            days_left = (item["due_date"] - date.today()).days
            if days_left < 0:
                urgency = f"⚠️ OVERDUE by {abs(days_left)} day(s)!"
            elif days_left == 0:
                urgency = "🔴 DUE TODAY!"
            else:
                urgency = f"📅 Due in {days_left} day(s)"

            wa_message = build_whatsapp_message(
                item['task'], str(item['due_date']), item['priority'], urgency
            )

            # Support both old single "phone" and new "phones" list
            phones = item.get("phones", [])
            if not phones and item.get("phone"):
                phones = [item["phone"]]

            if phones:
                # One button per saved number
                for num in phones:
                    wa_url = get_whatsapp_link(num, wa_message)
                    st.link_button(
                        f"📲 Send via WhatsApp ({num})",
                        wa_url,
                        use_container_width=True
                    )
            else:
                # No number saved — let user pick contact in WhatsApp
                wa_url = get_whatsapp_link_no_number(wa_message)
                st.link_button(
                    "📲 Send via WhatsApp",
                    wa_url,
                    use_container_width=True
                )

        # ---- Send to a Custom / Extra Number ----
        toggle_key = f"toggle_extra_{index}"
        extra_key = f"extra_number_{index}"

        if st.button(
            "📤 Send to a Different Number",
            key=toggle_key,
            use_container_width=False
        ):
            current = st.session_state.show_extra_number.get(index, False)
            st.session_state.show_extra_number[index] = not current

        if st.session_state.show_extra_number.get(index, False):
            with st.container():
                st.caption("Enter a number and click the link to open WhatsApp")
                extra_number_input = st.text_input(
                    "WhatsApp number (with country code)",
                    placeholder="+919876543210",
                    key=extra_key
                )
                if extra_number_input.strip():
                    custom_url = get_whatsapp_link(extra_number_input.strip(), wa_message)
                    st.link_button(
                        f"📩 Open WhatsApp for {extra_number_input.strip()}",
                        custom_url,
                        use_container_width=True
                    )
                else:
                    # No number entered — let user pick contact themselves
                    pick_url = get_whatsapp_link_no_number(wa_message)
                    st.link_button(
                        "📩 Open WhatsApp (pick contact yourself)",
                        pick_url,
                        use_container_width=True
                    )

        st.divider()


# ---------------- PRODUCTIVITY MESSAGE ----------------

st.subheader("Productivity")

if total == 0:

    st.info("Start by adding your first deadline.")

elif overdue > 0:

    st.warning(
        "You have " + str(overdue) +
        " overdue task(s). Try completing them first."
    )

elif completed == total:

    st.success(
        "Excellent! All your deadlines are completed."
    )

else:

    st.success(
        "You are making progress. Keep going."
    )