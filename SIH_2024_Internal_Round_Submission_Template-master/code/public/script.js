const currentTime = document.querySelector("h1"),
    content = document.querySelector(".content"),
    selectMenu = document.querySelectorAll("select"),
    setAlarmBtn = document.querySelector("button");
const snoozeBtn = document.getElementById("snoozeBtn"); // Add reference to Snooze button
let alarmTime,
    isAlarmSet,
    ringtone = new Audio("./files/ringtone.mp3");

// Populate the hour, minute, and AM/PM dropdowns
for (let i = 12; i > 0; i--) {
    i = i < 10 ? `0${i}` : i;
    let option = `<option value="${i}">${i}</option>`;
    selectMenu[0].firstElementChild.insertAdjacentHTML("afterend", option);
}
for (let i = 59; i >= 0; i--) {
    i = i < 10 ? `0${i}` : i;
    let option = `<option value="${i}">${i}</option>`;
    selectMenu[1].firstElementChild.insertAdjacentHTML("afterend", option);
}
for (let i = 2; i > 0; i--) {
    let ampm = i == 1 ? "AM" : "PM";
    let option = `<option value="${ampm}">${ampm}</option>`;
    selectMenu[2].firstElementChild.insertAdjacentHTML("afterend", option);
}

// Update the current time display every second
setInterval(() => {
    let date = new Date(),
        h = date.getHours(),
        m = date.getMinutes(),
        s = date.getSeconds(),
        ampm = "AM";
    if (h >= 12) {
        h = h - 12;
        ampm = "PM";
    }
    h = h == 0 ? (h = 12) : h;
    h = h < 10 ? "0" + h : h;
    m = m < 10 ? "0" + m : m;
    s = s < 10 ? "0" + s : s;
    currentTime.innerText = `${h}:${m}:${s} ${ampm}`;

    // Check if the current time matches the set alarm time
    if (alarmTime === `${h}:${m} ${ampm}`) {
        ringtone.play();
        ringtone.loop = true;
        snoozeBtn.style.display = 'block'; // Show Snooze button when alarm rings
    }
}, 1000);

// Set or clear the alarm
function setAlarm() {
    if (isAlarmSet) {
        alarmTime = "";
        ringtone.pause();
        content.classList.remove("disable");
        setAlarmBtn.innerText = "Set Alarm";
        isAlarmSet = false;
        snoozeBtn.style.display = 'none'; // Hide Snooze button when alarm is cleared
    } else {
        let time = `${selectMenu[0].value}:${selectMenu[1].value} ${selectMenu[2].value}`;
        if (
            time.includes("Hour") ||
            time.includes("Minute") ||
            time.includes("AM/PM")
        ) {
            return alert("Please, select a valid time to set Alarm!");
        }
        alarmTime = time;
        isAlarmSet = true;
        content.classList.add("disable");
        setAlarmBtn.innerText = "Clear Alarm";
        snoozeBtn.style.display = 'none'; // Ensure Snooze button is hidden until alarm goes off

        // Send the alarm time to the server via fetch
        fetch('/set-alarm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ alarmTime: time })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    }
}

// Add the click event listener to the Set Alarm button
setAlarmBtn.addEventListener("click", setAlarm);

// Snooze the alarm by adding 30 minutes to the current alarm time
function snoozeAlarm() {
    if (alarmTime) {
        let [time, ampm] = alarmTime.split(' ');
        let [hour, minute] = time.split(':').map(Number);

        minute += 30;
        if (minute >= 60) {
            minute -= 60;
            hour += 1;
        }

        if (hour > 12) {
            hour -= 12;
            ampm = ampm === 'AM' ? 'PM' : 'AM';
        }

        alarmTime = `${hour < 10 ? '0' + hour : hour}:${minute < 10 ? '0' + minute : minute} ${ampm}`;
        ringtone.pause();
        ringtone.currentTime = 0;
        isAlarmSet = true;
        snoozeBtn.style.display = 'none'; // Hide Snooze button until next alarm
        alert(`Alarm snoozed to ${alarmTime}`);
    }
}

// Add the click event listener to the Snooze button
snoozeBtn.addEventListener("click", snoozeAlarm);
