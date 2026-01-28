job Orchestrator

context State {
    count: 0,
    threshold: 3,
    status: "working"
}

conversion Voice {
    base: "Agent status is {status}. Count is {count}."
}

task Increment(amount) {
    context.count = context.count + amount
    say "Incremented count to {count}"
}

task Main() {
    say "Starting orchestration..."
    
    while context.count < context.threshold {
        call Increment(amount = 1)
        if context.count >= context.threshold {
            context.status = "done"
        }
    }
    
    say "Final status: {status}"
    success 0 "Orchestration Complete"
}
