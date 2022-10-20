#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# schemathesis.fixups.install(["fast_api"])
# schema = schemathesis.from_asgi('/openapi.json', app=app)
# state_machine = schema.as_state_machine()


# # @pytest.fixture(scope='session')
# # def build_database_schemathesis(database_engine):
# #     metadata = MetaData(database_engine)
# #     metadata.reflect()
# #     metadata.drop_all()
# #     sa_registry.metadata.create_all(database_engine)
# #     yield
# #     sa_registry.metadata.drop_all(database_engine)


# # @pytest.mark.slow
# # @schema.parametrize()
# # def test_api(case, client, build_database_schemathesis):
# #     case.call_and_validate(session=client, checks=(not_a_server_error,))
