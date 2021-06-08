"""Extractive summarization using target pretrained model with defined output length.

This module gets target content, model, and expected length of the result from users,
and return(print) corresponding summarization result.

Example:
    $ ext_summarize.py [-h] [-m MODEL] [-l LENGTH] body

Attributes:
    available_models: List of the available pretrained models
        scibert: https://github.com/allenai/scibert
    available_models_src: Map between available pretrained model name and its source.
    length: Map between avaliable input length format and actual ratio value to convert.
    _params: Defined paraemters for summarization.
        {
            'body' (str): Target content to summarize
            'model' (str): Target model name to build language model (default: scibert)
            'length' (float): The ratio of sentences in final summary (default: 0.4)
        } 
"""

import argparse
from summarizer import Summarizer
from transformers import AutoConfig, AutoTokenizer, AutoModel

available_models = ['scibert']
available_models_src = {
    'scibert': 'allenai/scibert_scivocab_uncased'
}
length = {'short': 0.2, 'medium': 0.4, 'long': 0.6}

_params = {'body': None,
           'model': 'scibert',
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
    model_config = AutoConfig.from_pretrained(
        available_models_src[model_name])
    model_config.output_hidden_states = True
    tokenizer = AutoTokenizer.from_pretrained(
        available_models_src[model_name])
    model = AutoModel.from_pretrained(
        available_models_src[model_name], config=model_config)

    return model, tokenizer


def ext_summarize(model, tokenizer, body, length):
    """Extract summary from the body

    This function summarize extractive way, 
    user can set model, tokenizer, and the length of the summary.

    Args:
        model: Model instance to use
        tokenizer: Tokenizer instance to use
        body (string): Target content to summarize
        length (float): The ratio of sentences in final summary

    Returns:
        result (string): Summary which consists of key sentences in body.
    """
    summarizer = Summarizer(custom_model=model, custom_tokenizer=tokenizer)
    result = summarizer(body, ratio=length)

    return result


def main():
    set_params()
    model, tokenizer = get_model(_params['model'])
    result = ext_summarize(
        model, tokenizer, _params['body'], _params['length'])
    print(result)


if __name__ == '__main__':
    main()
