import click

import glob
import os
import pathlib
import pandas as pd

num = 0

@click.command()
@click.option(
    "--type", 
    default="csv", 
    help="The file type to merge, default is csv"
)
@click.option(
    "--in_path", 
    default=pathlib.Path.cwd(), 
    help="The path where files are stored, default is the working directory"
)
@click.option(
    "--out_path", 
    default=pathlib.Path.cwd(), 
    help="The path where the result file will be stored, default is the working directory"
)
@click.option(
    "--out_name",
    help="The name for the output file"
)
def merge_files(type, in_path, out_path, out_name):

    if type == "csv":
        _merge_csv(type, in_path, out_path, out_name)
    else:
        click.echo("File type not supported.")


def _merge_csv(type, in_path, out_path, out_name):
    files = glob.glob(f"{in_path}/**/*.{type}", recursive=True)
    _create_output_path(out_path)
    merged = _pd_get_merged_csv(files)
    out_name = _get_out_name(out_name)
    merged.to_csv(os.path.join(out_path, f"{out_name}.csv"), index = False)


def _create_output_path(out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)


def _pd_get_merged_csv(files):
    frames = []
    for file in files:
        df = pd.read_csv(file)
        frames.append(df)
    return pd.concat(frames)


def _get_out_name(out_name):
    if not out_name:
        global num
        num += 1
        out_name = f"Merged_{num}"
    return out_name

if __name__ == "__main__":
    merge_files()
