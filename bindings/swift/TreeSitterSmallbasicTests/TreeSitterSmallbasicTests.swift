import XCTest
import SwiftTreeSitter
import TreeSitterSmallbasic

final class TreeSitterSmallbasicTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_smallbasic())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Smallbasic grammar")
    }
}
