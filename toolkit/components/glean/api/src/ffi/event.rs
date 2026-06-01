// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

#![cfg(feature = "with_gecko")]

use nsstring::{nsACString, nsCString};
use thin_vec::ThinVec;

use crate::metrics::__glean_metric_maps as metric_maps;
use crate::private::EventRecordingError;

#[no_mangle]
pub extern "C" fn fog_event_record(
    id: u32,
    extra_keys: &ThinVec<nsCString>,
    extra_values: &ThinVec<nsCString>,
) {}

#[no_mangle]
pub unsafe extern "C" fn fog_event_test_has_value(id: u32, ping_name: &nsACString) -> bool {
    false
}

#[no_mangle]
pub extern "C" fn fog_event_test_get_error(id: u32, error_str: &mut nsACString) -> bool {
    false
}

/// FFI-compatible representation of recorded event data.
#[repr(C)]
pub struct FfiRecordedEvent {
    timestamp: u64,
    category: nsCString,
    name: nsCString,

    /// Array of extra data, keys and values are interleaved.
    extras: ThinVec<nsCString>,
}

#[no_mangle]
pub extern "C" fn fog_event_test_get_value(
    id: u32,
    ping_name: &nsACString,
    out_events: &mut ThinVec<FfiRecordedEvent>,
) {}
