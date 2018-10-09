var notes = [
    ["Propositional Logic", "01.humanlogic"],
    ["Logical Inference", "02.inference"],
    ["Logical Clauses", "03.clauses"],
    ["Automated Satisfyability Solver", "04.automatedsatsolver"],
    ["Satisfyability Solver, the Program", "05.satsolverprogram"],
    ["Optimizations for the Satisfyability Solver", "06.efficientsatsolver"],
    ["Introduction to First Order Logic (FOL)", "07.firstorderlogic"],
    ["Models in Logic Space", "08.logicmodels"],
    ["Logical Translation - First Order Logic to Propositional Logic", "09.foltoprop"],

]

notes_container = document.getElementById("notes-container")

for (var i in notes) {
    let n = notes[i]

    let note_container = document.createElement("a")
    notes_container.appendChild(note_container)
    note_container.classList.add("note-container")
    note_container.href = n[1] + ".html"

    let note_title = document.createElement("div")
    note_container.appendChild(note_title)
    note_title.classList.add("note-title")
    note_title.innerText = n[0]
}