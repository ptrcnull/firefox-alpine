// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![cfg(feature = "with_gecko")]

use nsstring::nsACString;

#[no_mangle]
pub extern "C" fn fog_boolean_test_has_value(id: u32, ping_name: &nsACString) -> bool {
    false
}

#[no_mangle]
pub extern "C" fn fog_boolean_test_get_value(id: u32, ping_name: &nsACString) -> bool {
    false
}

#[no_mangle]
pub extern "C" fn fog_boolean_test_get_error(id: u32, error_str: &mut nsACString) -> bool {
    false
}

#[no_mangle]
pub extern "C" fn fog_boolean_set(id: u32, value: bool) {}
