job CoffeeBot

context BotState {
    user_name: "Guest",
    coffee_type: "none",
    stock_count: "unknown",
    mood: "neutral"
}

conversion BaristaVoice {
    base_instruction: """
    You are a friendly barista talking to {user_name}.
    We currently have {stock_count} cups of coffee in stock.
    The customer seems {mood}.
    """
}

task Main() {
    ask "Welcome! What's your name? {user_name=}"
    say "Nice to meet you, {user_name}!"
    
    say "Checking our inventory..."
    exec "https://api.coffee-shop.com/stock" {
        filter: ["stock_count"]
    }
    
    say "We have {stock_count} items left. What would you like to order?"
    process input {
        extract: ["coffee_type", "mood"]
    }
    
    say "Got it! One {coffee_type} coming up. You seem {mood} today!"
    
    success 0 "Order processed"
}
