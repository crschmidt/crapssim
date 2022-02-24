#!/usr/bin/python

# Copyright 2022 Christopher Schmidt
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
from strats.basic import passline_amount, dontline, passline, dontpass_amount
from sim import TABLE_MIN

def dodont(player, point):
    passline_amount(TABLE_MIN+10)(player, point)
    dontline(player, point)
def dontdo(player, point):
    dontpass_amount(TABLE_MIN+10)(player, point)
    passline(player, point)
