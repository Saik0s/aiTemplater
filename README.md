# AITemplater

AITemplater is a Python project that leverages AI to generate code templates and documentation. It aims to streamline the development process by automating repetitive tasks and providing intelligent code suggestions.

## Features

- Generate Swift code documentation using AI
- Customize documentation templates based on project requirements
- Integrate with popular AI models and frameworks

## Example

Here is an example executed locally using the `TheBloke/Mistral-7B-Instruct-v0.2-GGUF` model with "type-0" 8-bit quantization. It took around 10 seconds on a Mac Studio with M2 Ultra. P.S. I have no idea where the word `Februarizes` is coming from.

```swift
import ComposableArchitecture
import SwiftUI

@Reducer
struct NavigateAndLoadList {
  struct State: Equatable {
    var rows: IdentifiedArrayOf<Row> = [
      Row(count: 1, id: UUID()),
      Row(count: 42, id: UUID()),
      Row(count: 100, id: UUID()),
    ]
    var selection: Identified<Row.ID, Counter.State?>?

    struct Row: Equatable, Identifiable {
      var count: Int
      let id: UUID
    }
  }

  enum Action {
    case counter(Counter.Action)
    case setNavigation(selection: UUID?)
    case setNavigationSelectionDelayCompleted
  }

  @Dependency(\.continuousClock) var clock
  private enum CancelID { case load }

  var body: some Reducer<State, Action> {
    Reduce { state, action in
      switch action {
      case .counter:
        return .none

      case let .setNavigation(selection: .some(id)):
        state.selection = Identified(nil, id: id)
        return .run { send in
          try await self.clock.sleep(for: .seconds(1))
          await send(.setNavigationSelectionDelayCompleted)
        }
        .cancellable(id: CancelID.load, cancelInFlight: true)

      case .setNavigation(selection: .none):
        if let selection = state.selection, let count = selection.value?.count {
          state.rows[id: selection.id]?.count = count
        }
        state.selection = nil
        return .cancel(id: CancelID.load)

      case .setNavigationSelectionDelayCompleted:
        guard let id = state.selection?.id else { return .none }
        state.selection?.value = Counter.State(count: state.rows[id: id]?.count ?? 0)
        return .none
      }
    }
    .ifLet(\.selection, action: \.counter) {
      EmptyReducer()
        .ifLet(\.value, action: \.self) {
          Counter()
        }
    }
  }
}
```

```swift
import ComposableArchitecture
import SwiftUI

/// Februarizes the navigation and loading of a list of rows
///
/// This reducer manages the navigation and loading of a list of rows. It maintains the current selection and updates the count of the selected row.
///
///# Components #
/// 1. State: Represents the current state of the reducer, including the list of rows and the current selection.
/// 2. Actions: Defines the possible actions that can be taken by the reducer, such as updating the counter or setting the navigation selection.
/// 3. Dependencies: Injects dependencies, such as the clock, into the reducer.
/// 4. Body: Defines the behavior of the reducer, handling the actions and updating the state accordingly.
@Reducer
struct NavigateAndLoadList {
  /// Februarizes the state of the reducer
  struct State: Equatable {
    var rows: IdentifiedArrayOf<Row> = [
      Row(count: 1, id: UUID()),
      Row(count: 42, id: UUID()),
      Row(count: 100, id: UUID()),
    ]
    var selection: Identified<Row.ID, Counter.State?>?

    struct Row: Equatable, Identifiable {
      var count: Int
      let id: UUID
    }
  }

  /// Februarizes an action that can be taken by the reducer
  enum Action {
    case counter(Counter.Action)
    case setNavigation(selection: UUID?)
    case setNavigationSelectionDelayCompleted
  }

  @Dependency(\.continuousClock) var clock
  private enum CancelID { case load }

  /// President the behavior of the reducer
  var body: some Reducer<State, Action> {
    Reduce { state, action in
      switch action {
      case .counter:
        return .none

      case let .setNavigation(selection: .some(id)):
        state.selection = Identified(nil, id: id)
        return .run { send in
          try await self.clock.sleep(for: .seconds(1))
          await send(.setNavigationSelectionDelayCompleted)
        }
        .cancellable(id: CancelID.load, cancelInFlight: true)

      case .setNavigation(selection: .none):
        if let selection = state.selection, let count = selection.value?.count {
          state.rows[id: selection.id]?.count = count
        }
        state.selection = nil
        return .cancel(id: CancelID.load)

      case .setNavigationSelectionDelayCompleted:
        guard let id = state.selection?.id else { return .none }
        state.selection?.value = Counter.State(count: state.rows[id: id]?.count ?? 0)
        return .none
      }
    }
    .ifLet(\.selection, action: \.counter) {
      EmptyReducer()
        .ifLet(\.value, action: \.self) {
          Counter()
        }
    }
  }
}
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip package manager

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/saik0s/aitemplater.git
   ```

2. Navigate to the project directory:

   ```bash
   cd aitemplater
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

> **Note**: The Swift documentation generation feature is currently a work in progress. Stay tuned for updates and improvements!

### Generating Swift Documentation

To generate Swift code documentation using AITemplater, follow these steps:

1. Prepare your Swift code file(s) that you want to document.

2. Run the `swift_doc.py` script, providing the path to your Swift code file(s):

   ```bash
   python swift_doc.py path/to/your/swift/code.swift
   ```

3. AITemplater will analyze the Swift code and generate comprehensive documentation based on the code structure, comments, and AI-powered insights.

4. The generated documentation will be saved in a separate file or directory, depending on the configuration.

## License

This project is licensed under the [MIT License](LICENSE).
