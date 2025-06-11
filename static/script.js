async function submitSlots() {
  const jsonData = JSON.parse(document.getElementById("input-json").value);
  await fetch("/slots", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(jsonData)
  });
  alert("Slots submitted.");
}

async function getSuggestions() {
  const duration = document.getElementById("duration").value;
  const res = await fetch(`/suggest?duration=${duration}`);
  const slots = await res.json();

  const table = document.getElementById("suggestions");
  table.innerHTML = "<tr><th>Free Time Slot</th><th>Action</th></tr>";

  slots.forEach(slot => {
    const row = table.insertRow();
    row.insertCell().innerText = `${slot[0]}–${slot[1]}`;
    const btn = document.createElement("button");
    btn.innerText = "Book";
    btn.onclick = () => bookSlot(slot, duration);
    row.insertCell().appendChild(btn);
  });
}

async function bookSlot(slot, duration) {
  await fetch("/book", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slot, duration })
  });
  alert("Slot booked.");
}

async function viewCalendar() {
  const userId = document.getElementById("calendar-user-id").value.trim();
  if (!userId) {
    alert("Please enter a user ID");
    return;
  }

  const res = await fetch(`/calendar/${userId}`);
  const data = await res.json();
  console.log(data);

  const { slots, booked_slots } = data;

  const calendarTable = document.getElementById("calendar-table");
  calendarTable.innerHTML = "<tr><th>Time Range</th><th>Status</th></tr>";

  const bookedSet = new Set((booked_slots || []).map(slot => slot.join("-")));
  const allSlots = [...slots, ...(booked_slots || [])];

  allSlots.forEach(slot => {
    const range = `${slot[0]}–${slot[1]}`;
    const status = bookedSet.has(slot.join("-")) ? "booked" : "busy";

    const row = calendarTable.insertRow();
    row.insertCell().innerText = range;
    row.insertCell().innerText = status;
  });
}
