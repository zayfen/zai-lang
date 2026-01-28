// Coffee Shop Example for AgentLang
context.shop_name = "Gravity Coffee"
say "Welcome to " + context.shop_name + "! How can I help you today?"

process input {
    extract: ["intent", "item", "size"]
}

if context.intent == "order" {
    if context.item == "" {
        say "What would you like to order?"
    } else {
        say "Sure, a " + context.size + " " + context.item + " is on the way!"
    }
} else {
    say "I am a coffee bot. I can help you order coffee."
}
