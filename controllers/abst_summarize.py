"""Abstractive summarization using target pretrained model with defined output length.

This module gets target content, model, and expected length of the result from users,
and return(print) generated summarization result.

Example:
    $ abst_summarize.py [-h] [-m MODEL] [-l LENGTH] body

Attributes:
    available_models: List of the available pretrained models
        distilbart: https://huggingface.co/sshleifer/distilbart-cnn-12-6
    available_models_src: Map between available pretrained model name and its source.
    length: Map between avaliable input length format and actual ratio value to convert.
    _params: Defined paraemters for summarization.
        {
            'body' (str): Target content to summarize
            'model' (str): Target model name to build language model (default: distilbart)
            'length' (float): The ratio of sentences in final summary (default: 0.4)
        } 
"""

import argparse
from transformers import BartTokenizer, BartForConditionalGeneration

available_models = ['distilbart']
available_models_src = {
    'distilbart': 'sshleifer/distilbart-cnn-12-6'
}
length = {'short': 0.2, 'medium': 0.4, 'long': 0.6}

_params = {'body': None,
           'model': 'distilbart',
           'length': 0.4}


def set_params():
    """Set model parameters using arguments from the command line
    Raises:
        ValueError: 
            1) Input model name is not in `available_models`.
            2) Input length is not in `length`.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('body', type=str, help="Target content to summarize")
    parser.add_argument('-m', '--model', type=str,
                        help="Target model name to build language model")
    parser.add_argument('-l', '--length', type=str,
                        help="Length of the result of the summarization")
    args = parser.parse_args()

    _params['body'] = args.body

    if args.model is None:
        pass
    elif args.model in available_models:
        _params['model'] = args.model
    else:
        raise ValueError(
            "{} is not supported model name.\n[Available model list]: {}"
            .format(args.model, ', '.join(available_models)))

    if args.length is None:
        pass
    elif args.length in length:
        _params['length'] = length[args.length]
    else:
        raise ValueError(
            "{} unexpected input format of length.\nAvailable length format: {}"
            .format(args.length, ', '.join(length.keys())))


def get_model(model_name=_params['model']):
    """Get model and tokenizer from pretrained model

    Args:
        model_name (string): The name of pretrained model to request.

    Returns:
        model: Instance of the requested model class
        tokenizer: Instance of the requested tokenizer class
    """
    tokenizer = BartTokenizer.from_pretrained(
        available_models_src[model_name])
    model = BartForConditionalGeneration.from_pretrained(
        available_models_src[model_name])

    return model, tokenizer


def remove_tags(output):
    """Remove <s></s> tags in outputs

    Args:
        output (string): Result of abstractive summary generateion

    Returns:
        output (string): Processed result without tags
    """
    return output[8:-4]


def abst_summarize(model, tokenizer, body, length):
    """Generate summary from the body

    This function summarize abstractive way, 
    user can set model, tokenizer, and the length of the summary.

    Args:
        model: Model instance to use
        tokenizer: Tokenizer instance to use
        body (string): Target content to summarize
        length (float): The ratio of sentences in final summary

    Returns:
        result (string): Summary which consists of generated sentences 
                        which contain key content of body.
    """
    inputs = tokenizer.encode(
        "summarize: " + body, return_tensors='pt',
        max_length=1024, truncation=True)
    outputs = model.generate(
        inputs, num_beams=4, early_stopping=True,
        max_length=int(1000*length), min_length=int(250*length))
    result = remove_tags(tokenizer.decode(outputs[0]))

    return result


def main():
    set_params()
    model, tokenizer = get_model(_params['model'])
    result = abst_summarize(
        model, tokenizer, _params['body'], _params['length'])
    print(result)


if __name__ == '__main__':
    main()
