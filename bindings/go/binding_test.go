package tree_sitter_smallbasic_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_smallbasic "github.com/comom87/tree-sitter-smallbasic/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_smallbasic.Language())
	if language == nil {
		t.Errorf("Error loading Smallbasic grammar")
	}
}
