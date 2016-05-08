on run {input, parameters}
  tell application "iTerm"
    activate
    select first window
    tell current window
      set newTab to (create tab with default profile)
      tell current session
        write text "vim"
      end tell
    end tell
  end tell
end run
