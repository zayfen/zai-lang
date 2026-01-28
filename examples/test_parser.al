job HelloAgent

context Profile {
    name: "Riven"
}

conversion Default {
    base: "Hello {name}."
}

task Main() {
    say "Hello {name}"
    process "Greet the user" {
        extract: ["name"]
    }
    success 0 "Done"
}
