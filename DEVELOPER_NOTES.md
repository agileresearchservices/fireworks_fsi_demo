# Developer Notes

## Technologies Used

1. Fireworks AI Python SDK
2. Flask for web server
3. Python virtual environment
4. Python 3.11.7
5. Cursor AI IDE for development and debugging.
6. Perpexity, and ChatGPT for research and development.

## Limitations

1. Flask application is not production-ready. It is a simple server for development purposes only.
2. Currently using the free tier of Fireworks AI, so there are rate limits.
3. Scalability concerns for real-time features

## Concerns

1. Data privacy and security  
  a. User images and data should not be stored or shared on public servers. Properly secure the application before deploying it.
2. AI-generated content moderation  
  a. As with any AI model, it is not perfect. It may generate false positives or negatives. There should be a human in the loop to review the output.
3. Performance optimization for large-scale usage  
  a. The current setup is only for development purposes. It is not optimized for large-scale usage.

## Observations

1. Initial testing is limited to a small set of example images. More comprehensive testing is needed.
2. Occasional false positives and false negatives when extracting information from images.
3. Prompt engineering helps but, it is not a silver bullet and requires contstant iteration and improvement.
4. LLama 3.2 with vision is a powerful model, but it still makes the occasional mistake.
5. A comparison to GPT-4o with vision seemed to perform better based on the small sample set I tested it with.
6. Development experience was easy and enjoyable.
7. Documentation is excellent.

## Future Improvements

1. Continuous testing and monitoring including prompt engineering and model selection, and perhaps even fine-tuning to better fit the customer's use case.
2. Convert to a more production-ready architecture.
3. Authentication and authorization.
4. Use a more robust and scalable backend framework.
5. Deploy to a public cloud service provider.
6. Implement security and compliance features.
7. Develop as a general purpose API service for use by multiple clients.
