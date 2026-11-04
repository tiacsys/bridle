# SPDX-FileCopyrightText: 2024-2026 TiaC Systems
# SPDX-FileCopyrightText: 2024 Sarah Renkhoff
# SPDX-License-Identifier: Apache-2.0

function _bridleUnpackPhase {
    runHook preUnpack
    cp -r @bridle@ bridle
    chmod +w -R bridle
    cd bridle
    @git@ init
    @git@ config user.email "foo@bar.com"
    @git@ config user.name "Foo"
    @git@ checkout -b fake-branch
    @git@ add -A
    @git@ commit -m "Fake Commnit"
    cd ..
    runHook postUnpack
}

unpackPhase=(_bridleUnpackPhase)
