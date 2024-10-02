// License: GPLv3 Copyright: 2022, Kovid Goyal, <kovid at kovidgoyal.net>

package tool

import (
	"fmt"

	"alatty/kittens/ask"
	"alatty/kittens/clipboard"
	"alatty/kittens/icat"
	"alatty/kittens/notify"
	"alatty/kittens/show_key"
	"alatty/kittens/ssh"
	"alatty/kittens/themes"
	"alatty/kittens/unicode_input"
	"alatty/tools/cli"
	"alatty/tools/cmd/at"
	"alatty/tools/cmd/benchmark"
	"alatty/tools/cmd/edit_in_alatty"
	"alatty/tools/cmd/mouse_demo"
	"alatty/tools/cmd/pytest"
	"alatty/tools/cmd/run_shell"
	"alatty/tools/cmd/show_error"
	"alatty/tools/cmd/update_self"
	"alatty/tools/tui"
	"alatty/tools/utils/images"
)

var _ = fmt.Print

func AlattyToolEntryPoints(root *cli.Command) {
	root.Add(cli.OptionSpec{
		Name: "--version", Type: "bool-set", Help: "The current kitten version."})
	tui.PrepareRootCmd(root)
	// @
	at.EntryPoint(root)
	// update-self
	update_self.EntryPoint(root)
	// edit-in-alatty
	edit_in_alatty.EntryPoint(root)
	// clipboard
	clipboard.EntryPoint(root)
	// icat
	icat.EntryPoint(root)
	// ssh
	ssh.EntryPoint(root)
	// unicode_input
	unicode_input.EntryPoint(root)
	// show_key
	show_key.EntryPoint(root)
	// mouse_demo
	root.AddSubCommand(&cli.Command{
		Name:             "mouse-demo",
		ShortDescription: "Demo the mouse handling alatty implements for terminal programs",
		OnlyArgsAllowed:  true,
		Run: func(cmd *cli.Command, args []string) (rc int, err error) {
			return mouse_demo.Run(args)
		},
	})
	// ask
	ask.EntryPoint(root)
	// notify
	notify.EntryPoint(root)
	// themes
	themes.EntryPoint(root)
	themes.ParseEntryPoint(root)
	// run-shell
	run_shell.EntryPoint(root)
	// show_error
	show_error.EntryPoint(root)
	// __pytest__
	pytest.EntryPoint(root)
	// __hold_till_enter__
	root.AddSubCommand(&cli.Command{
		Name:            "__hold_till_enter__",
		Hidden:          true,
		OnlyArgsAllowed: true,
		Run: func(cmd *cli.Command, args []string) (rc int, err error) {
			tui.ExecAndHoldTillEnter(args)
			return
		},
	})
	// __confirm_and_run_shebang__
	root.AddSubCommand(&cli.Command{
		Name:            "__confirm_and_run_shebang__",
		Hidden:          true,
		OnlyArgsAllowed: true,
		Run: func(cmd *cli.Command, args []string) (rc int, err error) {
			return confirm_and_run_shebang(args)
		},
	})
	// __convert_image__
	images.ConvertEntryPoint(root)
	// __generate_man_pages__
	root.AddSubCommand(&cli.Command{
		Name:            "__generate_man_pages__",
		Hidden:          true,
		OnlyArgsAllowed: true,
		Run: func(cmd *cli.Command, args []string) (rc int, err error) {
			q := root
			if len(args) > 0 {
				for _, scname := range args {
					sc := q.FindSubCommand(scname)
					if sc == nil {
						return 1, fmt.Errorf("No sub command named: %s found", scname)
					}
					if err = sc.GenerateManPages(1, true); err != nil {
						return 1, err
					}
				}
			} else {
				if err = q.GenerateManPages(1, false); err != nil {
					rc = 1
				}
			}
			return
		},
	})
	benchmark.EntryPoint(root)
}
