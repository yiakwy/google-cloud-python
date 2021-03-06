# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()


# ----------------------------------------------------------------------------
# Generate scheduler GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "scheduler",
    "v1beta1",
    config_path="artman_cloudscheduler_v1beta1.yaml",
    artman_output_name="cloudscheduler-v1beta1",
    include_protos=True,
)

excludes = ["README.rst", "nox.py", "setup.py", "docs/conf.py", "docs/index.rst"]
s.move(library, excludes=excludes)

s.replace(
    "google/cloud/scheduler_v1beta1/gapic/cloud_scheduler_client.py",
    "google-cloud-cloudscheduler",
    "google-cloud-scheduler",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=79, cov_level=80)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
