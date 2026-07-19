# Frida 17.0.0 Released (2025-05-17)
Source: https://frida.re/news/2025/05/17/frida-17-0-0-released/

Frida 17.0.0 Released
    ∞

    
    release

  

    
      17 May 2025

    

      oleavr

  

    After countless cups of coffee and fun coding sessions, @hsorbo and I are
excited to bring you Frida 17.0.0. After nearly three years since the last major
bump, and struggling to find the right time to make breaking changes, we decided
it is finally time to do so.

Runtime Bridges

The main thing that’s been bothering us for quite some time was the fact that
our runtime bridges, i.e. frida-{objc,swift,java}-bridge, were bundled with
Frida’s GumJS runtime. This came with some major pain points:

  - Inertia: Being tied to Frida’s release cycle.

  - Bloat: For users who don’t need a particular runtime bridge.

  - Scalability: We’d like to see bridges for all kinds of runtimes, but the more
we add to Frida the more we’ll struggle with inertia and bloat.

  - Discoverability: Community-maintained bridges being harder to discover, as
they require a different workflow for consumption.

I’ve been hesitant to stop bundling them though, as requiring a build step for
custom agents seemed like it would add too much friction. And the thought of
breaking examples in books, blog posts, CodeShare etc. didn’t sit well with
me either.

The friction aspect is why we introduced the frida.Compiler API back in
15.2, along with frida-tools shipping a CLI tool, frida-compile, built on
top of it. Our REPL was also improved to support loading .ts (TypeScript)
directly, making use of frida.Compiler behind the scenes.

That’s still an extra step though, which is too much for one-off scripts and
early prototyping work using the Frida REPL or frida-trace. And, it would
break a lot of examples. To remedy this, the just-released frida-tools 14.0.0
bakes the three bridges into its REPL and frida-trace agents.

Our bridges have also been migrated to ESM, so they can be consumed by the
latest versions of frida-compile. (Shout-out to @yotamN for migrating
frida-java-bridge ♥️)

Those of you building Frida from source may also notice an improvement in build
times. Since we’re no longer bundling the bridges, we could finally get rid of
Gum’s frida-compile dependency, and stop depending on Node.js + npm for Gum
itself.

We still had GumJS’ own runtime, which implements built-ins such as
console.log(), but porting it to ESM and simply baking in each module
individually meant we no longer needed a JavaScript bundler. This means faster
build times for Gum itself: on a Linux-powered i9-12900K system, builds dropped
from ~24s → ~6s.

You can see a quick reference tutorial inside bridges.

Legacy-style enumeration APIs

Back in the day, our synchronous enumeration APIs all looked like this:

Process.enumerateModules({
  onMatch(module) {
    console.log(module.name);
  },
  onComplete() {
  }
});

There was also an equivalent Sync-suffixed method, like
Process.enumerateModulesSync() for this particular example. The idea was that
the underlying implementation could become asynchronous, but for the time being
most of them weren’t, so the Sync-suffixed implementation was just a thin
wrapper around the asynchronous-looking API.

Later, as more and more platforms were supported, I realized that all of the
pretend asynchronous implementations turned out to always be quick and cheap
operations. So offering an asynchronous flavor was going to be pointless. And
for the few that were truly asynchronous from the beginning, like
Memory.scan(), it still made sense to have them stay that way.

I was hesitant to break the API though, so I opted to add a check to each
unsuffixed implementation, so it would behave like its Sync-suffixed counterpart
if the callbacks argument was omitted. Wanting to migrate users off the
old-style API, I made sure to update our TypeScript bindings so only the modern
flavors were included.

The equivalent in modern style would then look like this:

for (const module of Process.enumerateModules()) {
  console.log(module.name);
}

Where Process.enumerateModules() returns an array of Module objects.

These legacy-style APIs are now finally gone. Those of you writing your agents
in TypeScript won’t need to do anything, unless you’re using ancient versions of
our typings.

Memory read/write APIs

Back in the day, you’d access memory like this:

const playerHealthLocation = ptr('0x1234');
const playerHealth = Memory.readU32(playerHealthLocation);
Memory.writeU32(playerHealthLocation, 100);

The modern equivalent is:

const playerHealthLocation = ptr('0x1234');
const playerHealth = playerHealthLocation.readU32();
playerHealthLocation.writeU32(100);

Where each write-counterpart returns the NativePointer itself, to support
chaining:

const playerData = ptr('0x1234');
playerData
    .add(4).writeU32(13)
    .add(4).writeU16(37)
    .add(2).writeU16(42)
    ;

The legacy versions of these are now also gone, and have been gone from our
TypeScript bindings for as long as the legacy-style enumeration APIs. So this
change should also not be noticable to most of you.

Static Module APIs

Now for the breaking changes that also affect users who were current with the
TypeScript bindings, prior to 19.0.0, released together with Frida 17. The
following static Module methods are now gone:

  - Module.ensureInitialized()

  - Module.findBaseAddress()

  - Module.getBaseAddress()

  - Module.findExportByName()

  - Module.getExportByName()

  - Module.findSymbolByName()

  - Module.getSymbolByName()

These are all straight-forward to migrate away from.

But first, let’s cover the odd one out:

Module.getSymbolByName(null, 'open')

This is now accomplished like this:

Module.getGlobalExportByName('open')

For the rest, you first need to look up the Module, and then access the desired
property or method on it. For example, instead of:

Module.getExportByName('libc.so', 'open')

The new way is:

Process.getModuleByName('libc.so').getExportByName('open')

The equivalent for Module.getBaseAddress() is thus:

Process.getModuleByName('libc.so').base

This means there is now only one way to do Module introspection, and the API
design is such that we encourage you to write performant code. For example, in
the past you might have been tempted to do:

const openImpl = Process.getExportByName('libc.so', 'open');
const readImpl = Process.getExportByName('libc.so', 'read');

But now you’ll probably think twice before doing:

const openImpl = Process.getModuleByName('libc.so').getExportByName('open');
const readImpl = Process.getModuleByName('libc.so').getExportByName('read');

And instead do:

const libc = Process.getModuleByName('libc.so');
const openImpl = libc.getExportByName('open');
const readImpl = libc.getExportByName('read');

Which is both more readable and more performant.

Last but not least, the static enumeration APIs, such as
Module.enumerateExports(), are now also gone. These were however removed from
the TypeScript bindings way back, so most of you shouldn’t need to deal with
these. But if you do, the migration looks exactly the same as above.

EOF

So that’s about it. Happy hacking!


---

# Frida 16.0.0 Released (2022-10-08)
Source: https://frida.re/news/2022/10/08/frida-16-0-0-released/

Frida 16.0.0 Released
    ∞

    
    release

  

    
      08 Oct 2022

    

      oleavr

  

    Hope some of you are enjoying frida.Compiler! In case you have no idea what that
is, check out the 15.2.0 release notes.

Performance

Back in 15.2.0 there was something that bothered me about frida.Compiler: it
would take a few seconds just to compile a tiny “Hello World”, even on my
i9-12900K Linux workstation:

$ time frida-compile explore.ts -o _agent.js

real	0m1.491s
user	0m3.016s
sys	0m0.115s

After a lot of profiling and insane amounts of yak shaving, I finally
arrived at this:

$ time frida-compile explore.ts -o _agent.js

real	0m0.325s
user	0m0.244s
sys	0m0.109s

That’s quite a difference! This means on-the-fly compilation use-cases such as
frida -l explore.ts are now a lot smoother. More importantly though, it means
Frida-based tools can load user scripts this way without making their users
suffer through seconds of startup delay.

Snapshots

You might be wondering how we made our compiler so quick to start. If you take
a peek under the hood, you’ll see that it uses the TypeScript compiler. This is
quite a bit of code to parse and run at startup. Also, loading and processing
the .d.ts files that define all of the types involved is actually even more
expensive.

The first optimization that we implemented back in 15.2 was to simply use our
V8 runtime if it’s available. That alone gave us a nice speed boost. However,
after a bit of profiling it was clear that V8 realized that it’s dealing with
a heavy workload once we start processing the .d.ts files, and that resulted in
it spending a big chunk of time just optimizing the TypeScript compiler’s code.

This reminded me of a really cool V8 feature that I’d noticed a long time ago:
custom startup snapshots. Basically if we could warm up the TypeScript
compiler ahead of time and also pre-create all of the .d.ts source files when
building Frida, we could snapshot the VM’s state at that point and embed the
resulting startup snapshot. Then at runtime we can boot from the snapshot and
hit the ground running.

As part of implementing this, I extended GumJS so a snapshot can be passed to
create_script(), together with the source code of the agent. There is also
snapshot_script(), used to create the snapshot in the first place.

For example:

import frida

session = frida.attach(0)

snapshot = session.snapshot_script("const example = { magic: 42 };",
                                   warmup_script="true",
                                   runtime="v8")
print("Snapshot created! Size:", len(snapshot))

This snapshot could then be saved to a file and later loaded like this:

script = session.create_script("console.log(JSON.stringify(example));",
                               snapshot=snapshot,
                               runtime="v8")
script.load()

Note that snapshots need to be created on the same OS/architecture/V8 version
as they’re later going to be loaded on.

V8 10.x

Another exciting bit of news is that we’ve upgraded V8 to 10.x, which means we
get to enjoy the latest VM refinements and JavaScript language features.
Considering that our last upgrade was more than two years ago, it’s definitely a
solid upgrade this time around.

The curse of multiple build systems, part two

As you may recall from the 15.1.15 release notes, we were closer than ever
to reaching the milestone where all of Frida can be built with a single build
system. The only component left at that point was V8, which we used to build
using Google’s GN build system. I’m happy to report that we have finally reached
that milestone. We now have a brand new Meson build system for V8. Yay!

EOF

There’s also a bunch of other exciting changes, so definitely check out the
changelog below.

Enjoy!

Changelog

  - compiler: Use snapshot to reduce startup time.

  - compiler: Bump frida-compile and other dependencies.

  - Add support for JavaScript VM snapshots. This is only implemented by the V8
backend, as QuickJS does not currently support this.

  - Move debugger API from Session to Script. This is necessary since V8’s
debugger works on a per-Isolate basis, and we now need one Isolate per Script
in order to support snapshots.

  - server+portal: Fix daemon parent ready fail exit. Thanks @pachoo!

  - resource-compiler: Add support for compression. We make use of this for
frida.Compiler’s heap snapshot.

  - ipc: Bump UNIX socket buffer sizes for improved throughput.

  - meson: Promote frida-payload to public API. This allows implementing custom
payloads for use-cases where frida-agent and frida-gadget aren’t suitable.

  - windows: Move to Visual Studio 2022.

  - windows: Move toolchain/SDK logic to use granular SDKs.

  - windows: Do not rely on .py file association.

  - darwin: Fix compatibility with macOS 13 and iOS >= 15.6.1.

  - darwin: Use Apple’s libffi-trampolines.dylib if present, so we can support
iOS 15 and beyond. Thanks for the fun pair-programming sessions, @hsorbo!

  - fruity: Fix handling of USBMUXD_SOCKET_ADDRESS. Thanks @0x3c3e!

  - fruity: Drop support for USBMUXD_SERVER_* envvars. Thanks @as0ler!

  - droidy: Improve handling of ADB envvars. Thanks @0x3c3e!

  - java: (android) Fix ClassLinker offset detection on Android 11 & 12 (#264).
Thanks @sh4dowb!

  - java: (android) Fix early instrumentation on Android 13.

  - java: Handle methods and fields prefixed with $. Thanks @eybisi!

  - android: Move to NDK r25.

  - arm64: Optimize memory copy implementation.

  - stalker: Ensure EventSink gets stopped on teardown.

  - stalker: Fix ARM stack clobbering when branch involves a shift.

  - stalker: Handle ARM PC load involving shifted register.

  - stalker: Notify ARM observer when backpatches are applied.

  - stalker: Apply ARM backpatches when notified.

  - stalker: Add ARM support for switch block callback.

  - arm-reader: Expose disassemble_instruction_at().

  - thumb-reader: Expose disassemble_instruction_at().

  - memory: Realign API with current V8 semantics.

  - gumjs: Move V8 backend to one Isolate per script.

  - gumjs: Support passing V8 flags using an env var: FRIDA_V8_EXTRA_FLAGS.

  - gumjs: Use V8 write protection on Darwin/arm*.

  - gumjs: Add support for dynamically defined scripts.

  - prof: Support old system headers on Linux/MIPS.

  - devkit: Improve examples’ compilation docs on UNIX.

  - ci: Migrate remainder of the legacy CI to GitHub Actions.

  - quickjs: Fix use-after-free on error during module evaluation.

  - v8: Upgrade to latest V8 10.x.

  - v8: Add Meson build system.

  - usrsctp: Lower Windows requirement to XP, like the rest of our components.

  - xz: Avoid ANSI-era Windows API.

  - libc-shim: Support old system headers on Linux/MIPS.

  - glib: Add Linux libc fallbacks for MIPS.

  - Add config.mk option to be able to disable emulated agents on Android, to
allow building smaller binaries. Thanks @muhzii!

  - python: Drop Python 2 support, modernize code, add docstrings, typings, add CI
with modern tooling, and many other goodies. Thanks @yotamN!

  - python: Build Python wheels instead of eggs. Thanks @oriori1703!

  - python: Fix Device.get_bus(). The previous implementation called
_Device.get_bus(), which doesn’t exist. Thanks @oriori1703!

  - python: Move to the stable Python C API.

  - python: Add support for building from source, using a frida-core devkit.

  - python: Add support for the new snapshot APIs.

  - node: Add support for the new snapshot APIs.

  - node: Fix Electron v20 compatibility.
