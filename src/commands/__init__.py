import discord.message


class ActivatorType:
    equals = 0
    starts_with = 1


class CommandActivator:
    def __init__(self, activator_type: int, value: str, caseSensitive=False):
        self.case_sensitive = caseSensitive
        self.type = activator_type
        if not self.case_sensitive:
            self.value = value.lower()

    def check(self, message: discord.Message):
        # lower case the to check value, if the activator is not case sensitive
        if not self.case_sensitive:
            to_check_value = message.content.lower()

        if self.type == ActivatorType.equals:
            return to_check_value == self.value
        elif self.type == ActivatorType.starts_with:
            return to_check_value.startswith(self.value)
        else:
            return False


class Placeholder:
    author_name = "{{DC:MESSAGE:AUTHOR:NAME}}"

    @staticmethod
    def data(my_key: str):
        return "{{DATA:"+ my_key +"}}"


class Renderer:
    @staticmethod
    def render(text: str, message: discord.Message, data=None):
        text = text.replace(Placeholder.author_name, message.author.name)

        # check for data placeholders
        if data is not None:
            pos = 0
            while pos < len(text):
                data_start_key = "{{DATA:"
                data_end_key = "}}"
                start_pos = text[pos:].find(data_start_key)
                if start_pos != -1:
                    start_pos += len(data_start_key) + pos
                    tmp = text[start_pos:]
                    end_pos = tmp.find(data_end_key)
                    if end_pos != -1:
                        end_pos += start_pos
                        found_data_key = text[start_pos:end_pos]
                        found_keys = found_data_key.split(".")
                        if len(found_keys) == 1:
                            if found_keys[0] in data.keys():
                                if data[found_keys[0]] is None:
                                    text = text.replace(data_start_key + found_data_key + "}}", "")
                                    pos += 0
                                else:
                                    text = text.replace(data_start_key + found_data_key + "}}", data[found_keys[0]])
                                    pos += len(data[found_keys[0]])
                        pos = end_pos + len(data_end_key)

                else:
                    pos = len(text)
        return text


class Command:
    activator: CommandActivator = None

    async def logic(self, message: discord.Message):
        pass

    async def handle(self, message: discord.Message):
        if self.activator.check(message):
            [message_to_send, data] = await self.logic(message)
            message_to_send = Renderer.render(message_to_send, message, data)
            await message.channel.send(message_to_send, reference=message, mention_author=False)
