import { Configuration, OpenAIApi } from "openai";
import { OPENAI_API_KEY } from "$env/static/private";
import { json, type RequestHandler } from "@sveltejs/kit";
import invariant from "tiny-invariant";

const configuration = new Configuration({
  apiKey: OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

export const POST: RequestHandler = async ({ request }) => {
  const { prompt } = await request.json();

  console.log("calling openai with prompt:", prompt);
  invariant(typeof prompt === "string", "Prompt required");

  const full_prompt = `@task The following quotes are grammatically incorrect followed by the correct intended quote. Correct the grammar of the incorrect quote, and predict several more words
  @exemplar "Walk dog" <I will take the dog for a walk>
  @exemplar "Book book two table" <There are two books on the table>
  @exemplar "i want take kids" <I want to take the kids to the park>
  @exemplar "sweaty i need" <I am sweaty and I need a hot shower>
  @exemplar "cat seems cat" <The cat seems hungry>
  @exemplar "i i need i need some" <I need to get some sleep>
  @exemplar "${prompt.trim()}" <`;

  const response = await openai.createCompletion({
    model: "text-davinci-002",
    prompt: full_prompt,
    temperature: 0.7,
    max_tokens: 256,
    n: 3,
    stop: ">",
  });

  // return list of completions
  const texts = response.data.choices.map((choice) => choice.text);
  return json({
    texts,
  });
};
