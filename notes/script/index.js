var notes = [
    ["Propositional Logic",
        "01.humanlogic"],
    ["Logical Inference",
        "02.inference"],
    ["Logical Clauses",
        "03.clauses"],
    ["Automated Satisfyability Solver",
        "04.automatedsatsolver"],
    ["Satisfyability Solver, the Program",
        "05.satsolverprogram"],
    ["Optimizations for the Satisfyability Solver",
        "06.efficientsatsolver"],
    ["Introduction to First Order Logic (FOL)",
        "07.firstorderlogic"],
    ["Models in Logic Space",
        "08.logicmodels"],
    ["Translating FOL to Propositional Logic",
        "09.foltoprop"],
    ["Introduction to Search",
        "10.introsearch"],
    ["State Spaces",
        "11.statespaces"],
    ["Search Algorithms",
        "12.searchalgorithms"],
    ["Search Algorithms Continued",
        "13.searchingcont"],
    ["The A* Algorithm",
        "14.astar"],
    ["Hueristics",
        "15.heuristics"],
    ["The Traveling Salesman Problem",
        "16.travelingsalesman"],
    ["Search Project Solutions",
        "17.searchsolution"],
    ["Adversarial Search",
        "18.adversarialsearch"],
    ["The MiniMax Algorithm",
        "19.minimax"],
    ["The ExpectiMax Algorithm",
        "20.expectimax"],
    ["Introduction to Reinforcement Learning",
        "21.reinforcementlearning"],
    ["Markov Desicion Process (MDP)",
        "22.marvokdesicions"],
    ["Value Iteration",
        "23.valueiteration"],
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