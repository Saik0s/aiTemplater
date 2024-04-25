import os
import time

import guidance
from guidance import gen, instruction, models, select
from huggingface_hub import hf_hub_download

repo_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
filename = "mistral-7b-instruct-v0.2.Q8_0.gguf"
model_kwargs = {"verbose": True, "n_gpu_layers": 32, "n_ctx": 32768, "n_threads": 20}

downloaded_file = hf_hub_download(repo_id=repo_id, filename=filename)
lm = guidance.models.LlamaCpp(downloaded_file, **model_kwargs)

temperature = 0.0
max_tokens = 300
stop_prefix = "\n[ \t]*[^/]"

a = time.time()

lm += f"""\
Analyze Swift code. Create concise, comprehensive docs. Enhance readability and maintainability. Cover:

1. Purpose: Summarize functionality and objectives.
2. Functions/Methods: Explain purpose, inputs, outputs, side effects. Use clear names.
3. Structure: Highlight component interactions, dependencies, control flow, design patterns.
4. Edge Cases/Errors: Document handling of exceptions and actions taken.
5. Performance: Discuss optimizations, trade-offs, decisions impacting speed.
6. Format/Style: Follow consistent swift doc comment style guide. Use clear, concise language. Proper formatting.
7. Be terse. No unnecessary words. No pleasantries. No apologies. Use short words.

Example:
```swift
/// Saves changes to the persistent store if the context has uncommitted changes
///
/// - parameter lastAPISync: Date data from the API was last synced.
/// - throws: An error is thrown if unsaved context changes cannot be committed to the persistent store
/// - returns: None
///
///# Notes: #
/// 1.  If a lastAPISync Date is provided, the lastAPISync date will be added and saved to the managedObjectContext
/// 2.  If there are no unsaved changes and no lastAPISync date is provided, this function does nothing.
func save(lastAPISync: Date?) throws
```

Here is provided code:
```swift
import ComposableArchitecture
import SwiftUI

@Reducer
struct NavigateAndLoadList {{
  struct State: Equatable {{
    var rows: IdentifiedArrayOf<Row> = [
      Row(count: 1, id: UUID()),
      Row(count: 42, id: UUID()),
      Row(count: 100, id: UUID()),
    ]
    var selection: Identified<Row.ID, Counter.State?>?

    struct Row: Equatable, Identifiable {{
      var count: Int
      let id: UUID
    }}
  }}

  enum Action {{
    case counter(Counter.Action)
    case setNavigation(selection: UUID?)
    case setNavigationSelectionDelayCompleted
  }}

  @Dependency(\.continuousClock) var clock
  private enum CancelID {{ case load }}

  var body: some Reducer<State, Action> {{
    Reduce {{ state, action in
      switch action {{
      case .counter:
        return .none

      case let .setNavigation(selection: .some(id)):
        state.selection = Identified(nil, id: id)
        return .run {{ send in
          try await self.clock.sleep(for: .seconds(1))
          await send(.setNavigationSelectionDelayCompleted)
        }}
        .cancellable(id: CancelID.load, cancelInFlight: true)

      case .setNavigation(selection: .none):
        if let selection = state.selection, let count = selection.value?.count {{
          state.rows[id: selection.id]?.count = count
        }}
        state.selection = nil
        return .cancel(id: CancelID.load)

      case .setNavigationSelectionDelayCompleted:
        guard let id = state.selection?.id else {{ return .none }}
        state.selection?.value = Counter.State(count: state.rows[id: id]?.count ?? 0)
        return .none
      }}
    }}
    .ifLet(\.selection, action: \.counter) {{
      EmptyReducer()
        .ifLet(\.value, action: \.self) {{
          Counter()
        }}
    }}
  }}
}}
```

Remember, the goal is to provide comprehensive and clear documentation that enhances the understanding and usability of the Swift code. The documentation should serve as a valuable resource for developers working with the codebase, enabling them to quickly grasp its functionality, make informed decisions, and maintain the code effectively over time.

Now generate the appropriate documentation for provided code based on the above guidelines.

```swift
import ComposableArchitecture
import SwiftUI

/// {gen(max_tokens=max_tokens, temperature=temperature, stop_regex=stop_prefix)}
@Reducer
struct NavigateAndLoadList {{
  /// {gen(max_tokens=max_tokens, temperature=temperature, stop_regex=stop_prefix)}
  struct State: Equatable {{
    var rows: IdentifiedArrayOf<Row> = [
      Row(count: 1, id: UUID()),
      Row(count: 42, id: UUID()),
      Row(count: 100, id: UUID()),
    ]
    var selection: Identified<Row.ID, Counter.State?>?

    struct Row: Equatable, Identifiable {{
      var count: Int
      let id: UUID
    }}
  }}

  /// {gen(max_tokens=max_tokens, temperature=temperature, stop_regex=stop_prefix)}
  enum Action {{
    case counter(Counter.Action)
    case setNavigation(selection: UUID?)
    case setNavigationSelectionDelayCompleted
  }}

  @Dependency(\.continuousClock) var clock
  private enum CancelID {{ case load }}

  /// {gen(max_tokens=max_tokens, temperature=temperature, stop_regex=stop_prefix)}
  var body: some Reducer<State, Action> {{
    Reduce {{ state, action in
      switch action {{
      case .counter:
        return .none

      case let .setNavigation(selection: .some(id)):
        state.selection = Identified(nil, id: id)
        return .run {{ send in
          try await self.clock.sleep(for: .seconds(1))
          await send(.setNavigationSelectionDelayCompleted)
        }}
        .cancellable(id: CancelID.load, cancelInFlight: true)

      case .setNavigation(selection: .none):
        if let selection = state.selection, let count = selection.value?.count {{
          state.rows[id: selection.id]?.count = count
        }}
        state.selection = nil
        return .cancel(id: CancelID.load)

      case .setNavigationSelectionDelayCompleted:
        guard let id = state.selection?.id else {{ return .none }}
        state.selection?.value = Counter.State(count: state.rows[id: id]?.count ?? 0)
        return .none
      }}
    }}
    .ifLet(\.selection, action: \.counter) {{
      EmptyReducer()
        .ifLet(\.value, action: \.self) {{
          Counter()
        }}
    }}
  }}
}}
```
"""

print(lm)
print(time.time() - a)
