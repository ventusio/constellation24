
import { z } from 'zod'


function destructEnv<T>(keys: (keyof T)[]): T {
  const result: T = {} as T
  keys.forEach((key) => {
    result[key] = process.env[key as string] as T[keyof T]
  })
  return result
}

// This method id needed because on cloudflare edge, we cannot destructure process.env so we need to return a new object
function destructEnvFromSchema<T extends z.AnyZodObject>(schema: T): z.infer<T> {
  const result = destructEnv(Object.keys(schema.shape))
  return schema.parse(result)
}


const envSchema = z.object({
  API_BASE_URL: z.string().default('http://localhost:8000'),
})

export const env = destructEnvFromSchema(envSchema)